"""Opt-in, local-only workflow timing for timed user studies.

Off by default, enabled per project. When on, per-scan workflow events are written to the
project's own SQLite database (table ``desktop_timing_events``); nothing is transmitted
anywhere. Active time counts only intervals between consecutive user inputs (mouse, keyboard,
wheel) that are at most ``IDLE_GAP_S`` (60 s) apart, so idle periods are excluded.

Events: ``scan_open``, ``scan_close``, ``first_edit``, ``edit`` (tool, voxels changed per class),
``review_signoff`` (object, decision), ``active_time`` (seconds accrued since the last flush).
"""
from __future__ import annotations

import csv
import json
import time
import uuid
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, QTimer

IDLE_GAP_S = 60.0
FLUSH_EVERY_S = 300

SCHEMA = """
CREATE TABLE IF NOT EXISTS desktop_settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS desktop_timing_events (
  id INTEGER PRIMARY KEY, session_id TEXT NOT NULL, study_id INTEGER, scan_id INTEGER, user_id INTEGER,
  event TEXT NOT NULL, tool TEXT, details TEXT, ts_utc TEXT NOT NULL);
"""

_INPUT_EVENTS = {QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseMove, QEvent.KeyPress,
                 QEvent.Wheel, QEvent.MouseButtonDblClick}


def _now_utc() -> str:
    t = time.time()
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(t)) + f".{int(t * 1000) % 1000:03d}Z"


class TimingRecorder:
    """Non-widget recorder bound to one project. ``clock`` is injectable for tests."""

    def __init__(self, project, clock=time.monotonic):
        self.project = project
        self.clock = clock
        self.session_id = uuid.uuid4().hex[:12]
        with project.store.lock:
            project.store.conn.executescript(SCHEMA)
        self.scan_id = None
        self.study_id = None
        self._last_input = None
        self._active = 0.0
        self._edited_scans: set = set()

    # ------------------------------------------------------------------ setting
    @property
    def enabled(self) -> bool:
        r = self.project.store.q1("SELECT value FROM desktop_settings WHERE key='workflow_timing'")
        return bool(r and r["value"] == "1")

    def set_enabled(self, on: bool):
        if not on:
            self.flush()
        self.project.store.exec("INSERT OR REPLACE INTO desktop_settings(key, value) VALUES ('workflow_timing', ?)",
                                ("1" if on else "0",))
        u = self.project.user
        self.project.store.audit.record("settings.workflow_timing", u["id"], u["org_id"], details={"enabled": bool(on)})
        if on:
            self._last_input = None
            self._active = 0.0

    # ------------------------------------------------------------------ events
    def _write(self, event, tool=None, details=None, scan_id=None):
        if not self.enabled:
            return
        u = self.project.user or {}
        self.project.store.exec(
            "INSERT INTO desktop_timing_events(session_id,study_id,scan_id,user_id,event,tool,details,ts_utc) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (self.session_id, self.study_id, self.scan_id if scan_id is None else scan_id, u.get("id"), event, tool,
             json.dumps(details or {}, default=str), _now_utc()))

    def input_activity(self):
        now = self.clock()
        if self._last_input is not None:
            gap = now - self._last_input
            if 0 < gap <= IDLE_GAP_S:
                self._active += gap
        self._last_input = now

    def flush(self):
        if self._active > 0 and self.scan_id is not None:
            self._write("active_time", details={"seconds": round(self._active, 3), "idle_gap_s": IDLE_GAP_S})
        self._active = 0.0

    def scan_opened(self, scan_id, study_id=None):
        self.flush()
        if self.scan_id is not None and self.scan_id != scan_id:
            self._write("scan_close")
        self.scan_id, self.study_id = scan_id, study_id
        self._last_input = self.clock()
        self._write("scan_open")

    def scan_closed(self):
        self.flush()
        if self.scan_id is not None:
            self._write("scan_close")
        self.scan_id = None

    def edit(self, tool: str, class_delta: dict):
        if self.scan_id is None or not self.enabled:
            return
        if self.scan_id not in self._edited_scans:
            self._edited_scans.add(self.scan_id)
            self._write("first_edit", tool)
        self._write("edit", tool, {"voxels_changed": {str(k): int(v) for k, v in class_delta.items()}})

    def signoff(self, object_type, object_id, decision):
        self._write("review_signoff", details={"object_type": object_type, "object_id": object_id, "decision": decision})

    # ------------------------------------------------------------------ export
    def events(self, study_id=None) -> list[dict]:
        with self.project.store.lock:
            self.project.store.conn.executescript(SCHEMA)
        q = "SELECT * FROM desktop_timing_events"
        args = ()
        if study_id is not None:
            q += " WHERE study_id=?"
            args = (study_id,)
        rows = self.project.store.q(q + " ORDER BY id", args)
        for r in rows:
            r["details"] = json.loads(r["details"] or "{}")
        return rows

    def summary(self, study_id=None) -> list[dict]:
        per: dict = {}
        for e in self.events(study_id):
            if e["scan_id"] is None:
                continue
            s = per.setdefault((e["scan_id"], e["user_id"]), {
                "scan_id": e["scan_id"], "study_id": e["study_id"], "user_id": e["user_id"], "opens": 0,
                "first_open_utc": None, "first_edit_utc": None, "edits": 0, "tools": {}, "voxels_changed": {},
                "signoffs": 0, "last_signoff_utc": None, "active_seconds": 0.0})
            ev = e["event"]
            if ev == "scan_open":
                s["opens"] += 1
                s["first_open_utc"] = s["first_open_utc"] or e["ts_utc"]
            elif ev == "first_edit":
                s["first_edit_utc"] = s["first_edit_utc"] or e["ts_utc"]
            elif ev == "edit":
                s["edits"] += 1
                s["tools"][e["tool"]] = s["tools"].get(e["tool"], 0) + 1
                for k, v in e["details"].get("voxels_changed", {}).items():
                    s["voxels_changed"][k] = s["voxels_changed"].get(k, 0) + v
            elif ev == "review_signoff":
                s["signoffs"] += 1
                s["last_signoff_utc"] = e["ts_utc"]
            elif ev == "active_time":
                s["active_seconds"] += float(e["details"].get("seconds", 0))
        return list(per.values())

    def export_csv(self, path, study_id=None) -> tuple[str, str]:
        """Writes ``path`` (one row per scan and user) and ``<path>_events.csv`` (raw events)."""
        from .. import LABELS
        path = Path(path)
        rows = self.summary(study_id)
        users = {u["id"]: u["username"] for u in self.project.store.q("SELECT id, username FROM users")}
        cls = [LABELS[c] for c in sorted(LABELS)]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["scan_id", "study_id", "user", "opens", "first_open_utc", "first_edit_utc", "edits",
                        "tools", "signoffs", "last_signoff_utc", "active_seconds"] + [f"voxels_changed_{c}" for c in cls])
            for r in rows:
                vc = {LABELS.get(int(k), k): v for k, v in r["voxels_changed"].items()}
                w.writerow([r["scan_id"], r["study_id"], users.get(r["user_id"], r["user_id"]), r["opens"],
                            r["first_open_utc"], r["first_edit_utc"], r["edits"],
                            ";".join(f"{k}:{v}" for k, v in sorted(r["tools"].items())), r["signoffs"],
                            r["last_signoff_utc"], round(r["active_seconds"], 1)] + [vc.get(c, 0) for c in cls])
        ev_path = path.with_name(path.stem + "_events.csv")
        with open(ev_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "session_id", "study_id", "scan_id", "user", "event", "tool", "details", "ts_utc"])
            for e in self.events(study_id):
                w.writerow([e["id"], e["session_id"], e["study_id"], e["scan_id"], users.get(e["user_id"], e["user_id"]),
                            e["event"], e["tool"] or "", json.dumps(e["details"]), e["ts_utc"]])
        u = self.project.user
        self.project.store.audit.record("timing.export", u["id"], u["org_id"], "study", study_id,
                                        {"path": str(path), "rows": len(rows)})
        return str(path), str(ev_path)


class ActivityFilter(QObject):
    """Application-wide event filter that feeds user-input activity to the recorder."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recorder: TimingRecorder | None = None
        self._enabled_cache = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._periodic)
        self._timer.start(FLUSH_EVERY_S * 1000)

    def set_recorder(self, rec):
        if self.recorder is not None:
            self.recorder.scan_closed()
        self.recorder = rec
        self.refresh()

    def refresh(self):
        self._enabled_cache = bool(self.recorder and self.recorder.enabled)

    def eventFilter(self, obj, ev):
        if self._enabled_cache and ev.type() in _INPUT_EVENTS and obj.isWidgetType():
            self.recorder.input_activity()
        return False

    def _periodic(self):
        if self._enabled_cache:
            self.recorder.flush()
