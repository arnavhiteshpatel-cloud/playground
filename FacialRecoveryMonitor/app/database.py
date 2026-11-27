"""Local SQLite storage.

All queries are parameterised. The schema is created on first launch with
``CREATE TABLE IF NOT EXISTS`` so existing records are never overwritten.
Timestamps are stored as local ISO-8601 strings (``YYYY-MM-DDTHH:MM:SS``).
"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional

from .config import APP_VERSION

log = logging.getLogger(__name__)

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    id                  INTEGER PRIMARY KEY CHECK (id = 1),
    display_name        TEXT,
    tracking_start_date TEXT,
    condition           TEXT,
    notes               TEXT,
    updated_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS checkin_sessions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at          TEXT NOT NULL,
    completed_at        TEXT NOT NULL,
    camera_index        INTEGER,
    landmarks_available INTEGER NOT NULL DEFAULT 0,
    images_saved        INTEGER NOT NULL DEFAULT 0,
    notes               TEXT,
    app_version         TEXT,
    created_at          TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS expression_records (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id        INTEGER NOT NULL REFERENCES checkin_sessions(id) ON DELETE CASCADE,
    step_order        INTEGER NOT NULL,
    expression_key    TEXT NOT NULL,
    expression_name   TEXT NOT NULL,
    status            TEXT NOT NULL
                      CHECK (status IN ('captured', 'skipped', 'no_face', 'not_analyzed')),
    captured_at       TEXT,
    frames_total      INTEGER NOT NULL DEFAULT 0,
    frames_with_face  INTEGER NOT NULL DEFAULT 0,
    head_yaw_deg      REAL,
    head_pitch_deg    REAL,
    head_roll_deg     REAL,
    features_json     TEXT,
    blendshapes_json  TEXT,
    image_path        TEXT
);

CREATE TABLE IF NOT EXISTS session_metrics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL REFERENCES checkin_sessions(id) ON DELETE CASCADE,
    metric_key  TEXT NOT NULL,
    label       TEXT NOT NULL,
    value       REAL NOT NULL,
    unit        TEXT,
    UNIQUE (session_id, metric_key)
);

CREATE TABLE IF NOT EXISTS symptom_surveys (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    completed_at  TEXT NOT NULL,
    notes         TEXT,
    app_version   TEXT,
    created_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS survey_responses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    survey_id       INTEGER NOT NULL REFERENCES symptom_surveys(id) ON DELETE CASCADE,
    question_key    TEXT NOT NULL,
    question_text   TEXT NOT NULL,
    category        TEXT NOT NULL,
    response_label  TEXT NOT NULL,
    response_score  INTEGER,
    UNIQUE (survey_id, question_key)
);

CREATE TABLE IF NOT EXISTS app_settings (
    key    TEXT PRIMARY KEY,
    value  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_completed ON checkin_sessions(completed_at);
CREATE INDEX IF NOT EXISTS idx_expr_session ON expression_records(session_id);
CREATE INDEX IF NOT EXISTS idx_metrics_session ON session_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_surveys_completed ON symptom_surveys(completed_at);
CREATE INDEX IF NOT EXISTS idx_responses_survey ON survey_responses(survey_id);
"""


class StorageError(Exception):
    """Raised with a user-readable message when the local database fails."""


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def parse_iso(value: str | None) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class Database:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self._lock = threading.RLock()
        try:
            if str(self.path) != ":memory:":
                self.path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.path), check_same_thread=False,
                                         detect_types=0, timeout=10)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("PRAGMA journal_mode = WAL")
            self._init_schema()
        except (sqlite3.Error, OSError) as exc:
            log.exception("Database initialisation failed")
            raise StorageError(
                f"The local database could not be opened or created at:\n{self.path}\n\n"
                f"Reason: {exc}") from exc

    # ------------------------------------------------------------------ basics
    def _init_schema(self) -> None:
        with self._lock:
            self._conn.executescript(SCHEMA)
            current = self._conn.execute("PRAGMA user_version").fetchone()[0]
            if current < SCHEMA_VERSION:
                self._conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            self._conn.commit()

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            try:
                with self._conn:
                    yield self._conn
            except sqlite3.Error as exc:
                log.exception("Database transaction failed")
                raise StorageError(f"Your data could not be saved to the local database. "
                                   f"Nothing was changed.\n\nReason: {exc}") from exc

    def _query(self, sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            try:
                return self._conn.execute(sql, tuple(params)).fetchall()
            except sqlite3.Error as exc:
                log.exception("Database query failed")
                raise StorageError(f"Your data could not be read from the local database.\n\n"
                                   f"Reason: {exc}") from exc

    def close(self) -> None:
        with self._lock:
            try:
                self._conn.close()
            except sqlite3.Error:
                pass

    # ----------------------------------------------------------------- settings
    def get_setting(self, key: str, default: Any = None) -> Any:
        rows = self._query("SELECT value FROM app_settings WHERE key = ?", (key,))
        if not rows:
            return default
        try:
            return json.loads(rows[0]["value"])
        except (TypeError, ValueError):
            return default

    def set_setting(self, key: str, value: Any) -> None:
        with self._tx() as c:
            c.execute("INSERT INTO app_settings(key, value) VALUES (?, ?) "
                      "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                      (key, json.dumps(value)))

    def delete_setting(self, key: str) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM app_settings WHERE key = ?", (key,))

    # ------------------------------------------------------------------ profile
    def get_profile(self) -> dict:
        rows = self._query("SELECT * FROM profile WHERE id = 1")
        if not rows:
            return {"display_name": "", "tracking_start_date": "", "condition": "",
                    "notes": "", "updated_at": None}
        return dict(rows[0])

    def save_profile(self, display_name: str, tracking_start_date: str, condition: str,
                     notes: str) -> None:
        with self._tx() as c:
            c.execute(
                "INSERT INTO profile(id, display_name, tracking_start_date, condition, notes, "
                "updated_at) VALUES (1, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET "
                "display_name = excluded.display_name, "
                "tracking_start_date = excluded.tracking_start_date, "
                "condition = excluded.condition, notes = excluded.notes, "
                "updated_at = excluded.updated_at",
                (display_name, tracking_start_date, condition, notes, now_iso()))

    # ---------------------------------------------------------------- check-ins
    def save_checkin(self, session: dict, expressions: list[dict], metrics: list[dict]) -> int:
        """Persist a check-in session, its expression records and derived metrics atomically."""
        with self._tx() as c:
            cur = c.execute(
                "INSERT INTO checkin_sessions(started_at, completed_at, camera_index, "
                "landmarks_available, images_saved, notes, app_version, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (session["started_at"], session["completed_at"], session.get("camera_index"),
                 int(bool(session.get("landmarks_available"))),
                 int(bool(session.get("images_saved"))), session.get("notes") or "",
                 APP_VERSION, now_iso()))
            sid = int(cur.lastrowid)
            for e in expressions:
                c.execute(
                    "INSERT INTO expression_records(session_id, step_order, expression_key, "
                    "expression_name, status, captured_at, frames_total, frames_with_face, "
                    "head_yaw_deg, head_pitch_deg, head_roll_deg, features_json, "
                    "blendshapes_json, image_path) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (sid, e["step_order"], e["expression_key"], e["expression_name"],
                     e["status"], e.get("captured_at"), int(e.get("frames_total") or 0),
                     int(e.get("frames_with_face") or 0), e.get("head_yaw_deg"),
                     e.get("head_pitch_deg"), e.get("head_roll_deg"),
                     json.dumps(e["features"]) if e.get("features") else None,
                     json.dumps(e["blendshapes"]) if e.get("blendshapes") else None,
                     e.get("image_path")))
            for m in metrics:
                if m.get("value") is None:
                    continue  # missing values are never stored as numbers
                c.execute(
                    "INSERT INTO session_metrics(session_id, metric_key, label, value, unit) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (sid, m["key"], m["label"], float(m["value"]), m.get("unit")))
        return sid

    def update_checkin_notes(self, session_id: int, notes: str) -> None:
        with self._tx() as c:
            c.execute("UPDATE checkin_sessions SET notes = ? WHERE id = ?", (notes, session_id))

    def list_checkins(self, since: str | None = None) -> list[dict]:
        sql = ("SELECT s.*, "
               "(SELECT COUNT(*) FROM expression_records e WHERE e.session_id = s.id "
               " AND e.status = 'captured') AS captured_count, "
               "(SELECT COUNT(*) FROM expression_records e WHERE e.session_id = s.id) "
               " AS expression_count, "
               "(SELECT COUNT(*) FROM session_metrics m WHERE m.session_id = s.id) "
               " AS metric_count "
               "FROM checkin_sessions s")
        params: list[Any] = []
        if since:
            sql += " WHERE s.completed_at >= ?"
            params.append(since)
        sql += " ORDER BY s.completed_at DESC, s.id DESC"
        return [dict(r) for r in self._query(sql, params)]

    def get_checkin(self, session_id: int) -> Optional[dict]:
        rows = self._query("SELECT * FROM checkin_sessions WHERE id = ?", (session_id,))
        if not rows:
            return None
        data = dict(rows[0])
        exprs = []
        for r in self._query("SELECT * FROM expression_records WHERE session_id = ? "
                             "ORDER BY step_order", (session_id,)):
            d = dict(r)
            d["features"] = json.loads(d.pop("features_json") or "null")
            d["blendshapes"] = json.loads(d.pop("blendshapes_json") or "null")
            exprs.append(d)
        data["expressions"] = exprs
        data["metrics"] = [dict(r) for r in self._query(
            "SELECT metric_key, label, value, unit FROM session_metrics WHERE session_id = ? "
            "ORDER BY id", (session_id,))]
        return data

    def delete_checkin(self, session_id: int) -> list[str]:
        """Delete a session (cascade) and return any image paths that belonged to it."""
        paths = [r["image_path"] for r in self._query(
            "SELECT image_path FROM expression_records WHERE session_id = ? "
            "AND image_path IS NOT NULL", (session_id,))]
        with self._tx() as c:
            c.execute("DELETE FROM checkin_sessions WHERE id = ?", (session_id,))
        return paths

    def metric_series(self, since: str | None = None) -> list[dict]:
        sql = ("SELECT s.id AS session_id, s.completed_at, m.metric_key, m.label, m.value, m.unit "
               "FROM session_metrics m JOIN checkin_sessions s ON s.id = m.session_id")
        params: list[Any] = []
        if since:
            sql += " WHERE s.completed_at >= ?"
            params.append(since)
        sql += " ORDER BY s.completed_at"
        return [dict(r) for r in self._query(sql, params)]

    def latest_checkin(self) -> Optional[dict]:
        rows = self._query("SELECT id FROM checkin_sessions ORDER BY completed_at DESC, id DESC "
                           "LIMIT 1")
        return self.get_checkin(rows[0]["id"]) if rows else None

    # ------------------------------------------------------------------ surveys
    def save_survey(self, completed_at: str, notes: str, responses: list[dict]) -> int:
        if not responses:
            raise StorageError("A survey must contain at least one response.")
        with self._tx() as c:
            cur = c.execute("INSERT INTO symptom_surveys(completed_at, notes, app_version, "
                            "created_at) VALUES (?, ?, ?, ?)",
                            (completed_at, notes or "", APP_VERSION, now_iso()))
            sid = int(cur.lastrowid)
            c.executemany(
                "INSERT INTO survey_responses(survey_id, question_key, question_text, category, "
                "response_label, response_score) VALUES (?, ?, ?, ?, ?, ?)",
                [(sid, r["question_key"], r["question_text"], r["category"],
                  r["response_label"], r.get("response_score")) for r in responses])
        return sid

    def list_surveys(self, since: str | None = None) -> list[dict]:
        sql = ("SELECT v.*, (SELECT COUNT(*) FROM survey_responses r WHERE r.survey_id = v.id) "
               "AS response_count FROM symptom_surveys v")
        params: list[Any] = []
        if since:
            sql += " WHERE v.completed_at >= ?"
            params.append(since)
        sql += " ORDER BY v.completed_at DESC, v.id DESC"
        return [dict(r) for r in self._query(sql, params)]

    def get_survey(self, survey_id: int) -> Optional[dict]:
        rows = self._query("SELECT * FROM symptom_surveys WHERE id = ?", (survey_id,))
        if not rows:
            return None
        data = dict(rows[0])
        data["responses"] = [dict(r) for r in self._query(
            "SELECT question_key, question_text, category, response_label, response_score "
            "FROM survey_responses WHERE survey_id = ? ORDER BY id", (survey_id,))]
        return data

    def latest_survey(self) -> Optional[dict]:
        rows = self._query("SELECT id FROM symptom_surveys ORDER BY completed_at DESC, id DESC "
                           "LIMIT 1")
        return self.get_survey(rows[0]["id"]) if rows else None

    def delete_survey(self, survey_id: int) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM symptom_surveys WHERE id = ?", (survey_id,))

    def survey_series(self, question_key: str, since: str | None = None) -> list[dict]:
        sql = ("SELECT v.id AS survey_id, v.completed_at, r.response_label, r.response_score "
               "FROM survey_responses r JOIN symptom_surveys v ON v.id = r.survey_id "
               "WHERE r.question_key = ?")
        params: list[Any] = [question_key]
        if since:
            sql += " AND v.completed_at >= ?"
            params.append(since)
        sql += " ORDER BY v.completed_at"
        return [dict(r) for r in self._query(sql, params)]

    # --------------------------------------------------------------- aggregates
    def summary(self) -> dict:
        checkins = self._query("SELECT COUNT(*) AS n, MIN(completed_at) AS first, "
                               "MAX(completed_at) AS last FROM checkin_sessions")[0]
        surveys = self._query("SELECT COUNT(*) AS n, MIN(completed_at) AS first, "
                              "MAX(completed_at) AS last FROM symptom_surveys")[0]
        firsts = [d for d in (checkins["first"], surveys["first"]) if d]
        lasts = [d for d in (checkins["last"], surveys["last"]) if d]
        return {
            "checkin_count": checkins["n"], "survey_count": surveys["n"],
            "last_checkin": checkins["last"], "last_survey": surveys["last"],
            "first_record": min(firsts) if firsts else None,
            "last_record": max(lasts) if lasts else None,
        }

    def activity(self, kind: str = "all", newest_first: bool = True,
                 limit: int | None = None) -> list[dict]:
        """Unified activity feed of check-ins and surveys."""
        items: list[dict] = []
        if kind in ("all", "checkin"):
            for s in self.list_checkins():
                items.append({"type": "checkin", "id": s["id"], "timestamp": s["completed_at"],
                              "captured": s["captured_count"], "total": s["expression_count"],
                              "metrics": s["metric_count"], "notes": s["notes"] or "",
                              "images_saved": bool(s["images_saved"])})
        if kind in ("all", "survey"):
            for v in self.list_surveys():
                items.append({"type": "survey", "id": v["id"], "timestamp": v["completed_at"],
                              "responses": v["response_count"], "notes": v["notes"] or ""})
        items.sort(key=lambda i: (i["timestamp"], i["id"]), reverse=newest_first)
        return items[:limit] if limit else items

    # ----------------------------------------------------------------- deletion
    def all_image_paths(self) -> list[str]:
        return [r["image_path"] for r in self._query(
            "SELECT image_path FROM expression_records WHERE image_path IS NOT NULL")]

    def delete_all_data(self, include_profile: bool = True) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM session_metrics")
            c.execute("DELETE FROM expression_records")
            c.execute("DELETE FROM checkin_sessions")
            c.execute("DELETE FROM survey_responses")
            c.execute("DELETE FROM symptom_surveys")
            c.execute("DELETE FROM app_settings WHERE key IN ('survey_draft', 'demo_dataset')")
            if include_profile:
                c.execute("DELETE FROM profile")
        with self._lock:
            try:
                self._conn.execute("VACUUM")
            except sqlite3.Error:
                log.warning("VACUUM after delete failed", exc_info=True)
