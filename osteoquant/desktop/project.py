"""Desktop project = a folder holding one study store (SQLite + chunked scan data).

Layout::

    <project>/
      osteoquant-project.json   marker: name, created, application version
      osteoquant.db             osteoquant.study.db.Store (users, studies, scans, audit trail)
      data/                     Zarr scan stores, reports, figures

Each project is its own organisation in the store. Signing in uses the store's users and
password policy; every action is attributed to the signed-in user in the audit trail.
"""
from __future__ import annotations

import json
import secrets
import time
from pathlib import Path

from .. import __version__
from ..study.db import Store, check_password

MARKER = "osteoquant-project.json"
DB_NAME = "osteoquant.db"

DESKTOP_SCHEMA = """
CREATE TABLE IF NOT EXISTS desktop_import_log (
  id INTEGER PRIMARY KEY, study_id INTEGER, source TEXT NOT NULL, status TEXT NOT NULL,
  reason TEXT, scan_id INTEGER, user_id INTEGER, details TEXT, created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS desktop_settings (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS desktop_blind_codes (
  object_type TEXT NOT NULL, object_id INTEGER NOT NULL, study_id INTEGER, code TEXT NOT NULL,
  created TEXT NOT NULL, PRIMARY KEY (object_type, object_id), UNIQUE (study_id, object_type, code));
CREATE TABLE IF NOT EXISTS desktop_review_meta (review_id INTEGER PRIMARY KEY, signature_role TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS desktop_report_meta (report_id INTEGER PRIMARY KEY, blinded INTEGER NOT NULL DEFAULT 0,
  bundle_path TEXT, signed_pdf TEXT, signed_sha256 TEXT);
"""
# columns added after the first desktop release (C2-PRD-04/05): SHA-256 of the report bundle recorded at
# generation, and the review status of the reported segmentations at generation
DESKTOP_COLUMNS = {"desktop_report_meta": [("bundle_sha256", "TEXT"), ("review_status", "TEXT")]}

# Roles offered in the desktop user administration (Store role id -> label shown to people).
ROLE_LABELS = {"analyst": "Analyst", "reviewer": "Reviewer", "study_director": "Study director", "admin": "Administrator",
               "viewer": "Viewer (read only)"}
# What each permission lets a person do, for disabled-action tooltips.
PERMISSION_TEXT = {"write": "import scans, run analyses, edit labels and define ROIs",
                   "run": "run analyses", "review": "sign reviews and approvals",
                   "manage_users": "manage user accounts", "unblind": "unblind studies", "export": "export data"}
# Blinded codes: unambiguous characters (no 0/O, 1/I/L), random per object, unique within a study.
_CODE_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
_CODE_PREFIX = {"scan": "S", "animal": "A"}


class ProjectError(RuntimeError):
    pass


def _roles() -> dict:
    from ..study.db import ROLES
    return ROLES


def is_project_folder(folder) -> bool:
    return (Path(folder) / MARKER).is_file() and (Path(folder) / DB_NAME).is_file()


class Project:
    def __init__(self, folder):
        self.integrity_problems: list[str] = []
        self.folder = Path(folder).resolve()
        if not is_project_folder(self.folder):
            raise ProjectError(f"{self.folder} is not an OsteoQuant project folder")
        self.meta = json.loads((self.folder / MARKER).read_text(encoding="utf-8"))
        self.store = Store(self.folder / DB_NAME, self.folder / "data")
        self.store.conn.executescript(DESKTOP_SCHEMA)
        for table, cols in DESKTOP_COLUMNS.items():
            have = {r[1] for r in self.store.conn.execute(f"PRAGMA table_info({table})")}
            for name, typ in cols:
                if name not in have:
                    self.store.conn.execute(f"ALTER TABLE {table} ADD COLUMN {name} {typ}")
        self.user: dict | None = None
        self._token: str | None = None
        self.session_end_reason: str | None = None

    # ------------------------------------------------------------------ lifecycle
    @classmethod
    def create(cls, folder, name: str, username: str, password: str, full_name: str = "") -> "Project":
        folder = Path(folder)
        if folder.exists() and any(folder.iterdir()):
            raise ProjectError("Choose an empty or new folder for a new project")
        from ..study.db import password_policy
        try:
            password_policy(password)
        except ValueError as e:
            raise ProjectError(str(e)) from e
        if not name.strip() or not username.strip():
            raise ProjectError("Project name and user name are required")
        folder.mkdir(parents=True, exist_ok=True)
        st = Store(folder / DB_NAME, folder / "data")
        oid = st.create_org(name)
        st.create_user(oid, username, password, "admin", full_name or username)
        st.conn.close()
        (folder / MARKER).write_text(json.dumps({
            "name": name, "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "created_with": f"OsteoQuant Desktop {__version__}", "format": 1}, indent=1), encoding="utf-8")
        p = cls(folder)
        if not p.login(username, password):
            raise ProjectError("Could not sign in to the new project")
        return p

    @property
    def name(self) -> str:
        return self.meta.get("name", self.folder.name)

    @property
    def data_dir(self) -> Path:
        return self.store.data_dir

    def close(self):
        if self._token:
            try:
                self.store.logout(self._token)
                self.store.audit.record("auth.logout", self.user["id"], self.user["org_id"])
            except Exception:  # noqa: BLE001 - closing must not fail
                pass
        self._token = None
        self.user = None
        try:
            self.store.conn.close()
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------ auth
    SESSION_TTL_S = 8 * 3600

    def login(self, username: str, password: str) -> bool:
        tok = self.store.login(username, password, ttl_s=self.SESSION_TTL_S)
        if not tok:
            return False
        self._token = tok
        self.user = self.store.validate_session(tok)
        self.session_end_reason = None
        # external anchors (C3-PRD-03): a mismatch disables electronic signatures and is recorded
        from .anchors import verify_anchors
        self.integrity_problems = verify_anchors(self.store)
        if self.integrity_problems and self.user:
            try:
                self.store.audit.record("audit.anchor_mismatch", self.user["id"], self.user["org_id"], "project", None,
                                        {"problems": self.integrity_problems[:5]})
            except Exception:  # noqa: BLE001 - recording must not block sign-in
                pass
        return self.user is not None

    @property
    def password_change_required(self) -> bool:
        return bool(self.user and self.user.get("must_change_password"))

    def check_session(self) -> bool:
        """Re-validate the session against the database (C2-PRD-07): a deactivated user, a password
        reset or a sign-out elsewhere ends it; a role change takes effect. Returns False (and drops the
        signed-in user) when the session has ended."""
        if not self.user:
            return False
        u = self.store.validate_session(self._token, sliding_ttl_s=self.SESSION_TTL_S)
        if u is None:
            row = self.store.q1("SELECT active FROM users WHERE id=?", (self.user["id"],))
            reason = ("your account was deactivated by an administrator" if row and not row["active"] else
                      "your session was ended (password reset by an administrator, or signed out)")
            try:
                self.store.audit.record("session.ended", self.user["id"], self.user["org_id"], "user", self.user["id"],
                                        {"reason": reason})
            except Exception:  # noqa: BLE001 - ending a session must not fail
                pass
            self.session_end_reason = reason
            self.user = None
            self._token = None
            return False
        if u["role"] != self.user["role"]:
            problem = self.store.user_record_problem(u)
            if problem:      # role edited outside the audited API: end the session (C2-PRD-09)
                self.store.audit.record("auth.user_record_mismatch", u["id"], u["org_id"], "user", u["id"],
                                        {"reason": problem})
                self.session_end_reason = "your account record failed its integrity check: " + problem
                self.store.logout(self._token)
                self.user = None
                self._token = None
                return False
        self.user.update(u)
        return True

    def reauthenticate(self, password: str, object_type=None, object_id=None) -> bool:
        """Re-check the signed-in user's password (used before electronic signatures)."""
        # Delegate to Store.reauthenticate so failures count towards the same temporary lockout as login
        # (cycle-1 finding: the desktop path previously bypassed the lockout fixed for the API).
        ok = self.store.reauthenticate(self.require_user(), password)
        if not ok:
            self.store.audit.record("review.reauth_failed", self.user["id"], self.user["org_id"], object_type, object_id)
        return ok

    def require_user(self) -> dict:
        """The signed-in user, re-validated against the database before every action (C2-PRD-07)."""
        if not self.user:
            raise ProjectError("Not signed in" + (f": {self.session_end_reason}" if self.session_end_reason else ""))
        if not self.check_session():
            raise ProjectError(f"Session ended: {self.session_end_reason}. Sign in again.")
        return self.user

    def can(self, perm: str) -> bool:
        return bool(self.user) and self.store.can(self.user, perm)

    def why_not(self, perm: str) -> str:
        """Tooltip text for an action the signed-in role cannot perform ('' when it can)."""
        if self.can(perm):
            return ""
        role = ROLE_LABELS.get((self.user or {}).get("role", ""), (self.user or {}).get("role", "?"))
        allowed = sorted(ROLE_LABELS[r] for r, perms in _roles().items() if perm in perms and r in ROLE_LABELS)
        return (f"Your role ({role}) cannot {PERMISSION_TEXT.get(perm, perm)}. "
                f"Requires: {', '.join(allowed)}.")

    # ------------------------------------------------------------------ settings (project-wide, audited)
    def setting(self, key: str, default=None):
        r = self.store.q1("SELECT value FROM desktop_settings WHERE key=?", (key,))
        return r["value"] if r else default

    def set_setting(self, key: str, value, audit_action: str | None = None):
        self.store.exec("INSERT OR REPLACE INTO desktop_settings(key, value) VALUES (?, ?)", (key, str(value)))
        if audit_action:
            u = self.require_user()
            self.store.audit.record(audit_action, u["id"], u["org_id"], details={"key": key, "value": str(value)})

    IDLE_LOCK_DEFAULT_MIN = 15

    @property
    def idle_lock_minutes(self) -> int:
        try:
            return max(0, int(float(self.setting("idle_lock_minutes", self.IDLE_LOCK_DEFAULT_MIN))))
        except (TypeError, ValueError):
            return self.IDLE_LOCK_DEFAULT_MIN

    def set_idle_lock_minutes(self, minutes: int):
        u = self.require_user()
        self.store.require(u, "manage_users")
        self.set_setting("idle_lock_minutes", int(minutes), "settings.idle_lock")

    # ------------------------------------------------------------------ user administration (admin only)
    def users(self) -> list[dict]:
        u = self.require_user()
        self.store.require(u, "manage_users")
        rows = self.store.q("SELECT id, username, full_name, role, active, failed_logins, locked_until, created FROM users "
                            "WHERE org_id=? ORDER BY id", (u["org_id"],))
        for r in rows:
            r["locked"] = (r.get("locked_until") or 0) > time.time()
        return rows

    def add_user(self, username: str, full_name: str, role: str, password: str) -> int:
        u = self.require_user()
        if not username.strip():
            raise ValueError("A user name is required")
        if self.store.q1("SELECT id FROM users WHERE username=?", (username.strip(),)):
            raise ValueError(f"The user name '{username.strip()}' is already taken")
        return self.store.create_user(u["org_id"], username.strip(), password, role, full_name.strip(), actor=u)

    def set_user_active(self, user_id: int, active: bool):
        u = self.require_user()
        if int(user_id) == int(u["id"]) and not active:
            raise ValueError("You cannot deactivate your own account while signed in")
        self.store.set_user_active(u, user_id, active)

    def reset_password(self, user_id: int, new_password: str):
        self.store.reset_password(self.require_user(), user_id, new_password)

    def set_user_role(self, user_id: int, role: str):
        self.store.set_user_role(self.require_user(), user_id, role)

    def change_password(self, old_password: str, new_password: str):
        """Self-service password change; this session continues, other sessions of the user end."""
        u = self.require_user()
        self.store.change_password(u, old_password, new_password)
        self.store.end_other_sessions(u["id"], self._token)
        self.user["must_change_password"] = 0

    # ------------------------------------------------------------------ study-level blinding (C2-PRD-03)
    def study_forces_blinding(self, study_id) -> bool:
        """True when ``study_id`` is flagged blinded and the signed-in role may not see allocation."""
        if study_id is None or not self.user:
            return False
        r = self.store.q1("SELECT blinded, org_id FROM studies WHERE id=?", (study_id,))
        return bool(r and r["blinded"]) and not self.can("unblind")

    def blinding_forced(self) -> bool:
        """True when any open study of the project is blinded and the signed-in role may not unblind:
        the whole desktop then stays in blinded review mode (the toggle is locked)."""
        if not self.user or self.can("unblind"):
            return False
        return bool(self.store.q1("SELECT 1 FROM studies WHERE org_id=? AND blinded=1 AND COALESCE(status,'')<>'deleted' "
                                  "LIMIT 1", (self.user["org_id"],)))

    def blinded_studies(self) -> list[dict]:
        u = self.require_user()
        return self.store.q("SELECT id, name FROM studies WHERE org_id=? AND blinded=1 AND COALESCE(status,'')<>'deleted' "
                            "ORDER BY id", (u["org_id"],))

    # ------------------------------------------------------------------ blinding
    def blind_code(self, kind: str, object_id, study_id=None) -> str:
        """Random, non-sequential code for a scan or animal, stored in the project (stable across
        sessions, unique within the study). Database IDs are never shown in blinded mode."""
        if object_id is None:
            return "unassigned"
        r = self.store.q1("SELECT code FROM desktop_blind_codes WHERE object_type=? AND object_id=?", (kind, int(object_id)))
        if r:
            return r["code"]
        from ..study.db import now
        for _ in range(50):
            code = f"{_CODE_PREFIX.get(kind, 'X')}-" + "".join(secrets.choice(_CODE_ALPHABET) for _ in range(4))
            try:
                with self.store.lock:
                    self.store.conn.execute("INSERT INTO desktop_blind_codes(object_type, object_id, study_id, code, created)"
                                            " VALUES (?,?,?,?,?)", (kind, int(object_id), study_id, code, now()))
                return code
            except Exception:  # noqa: BLE001 - code collision within the study: draw again
                r = self.store.q1("SELECT code FROM desktop_blind_codes WHERE object_type=? AND object_id=?",
                                  (kind, int(object_id)))
                if r:
                    return r["code"]
        raise ProjectError("Could not allocate a blinded code")

    def scan_code(self, scan_id, study_id=None) -> str:
        if study_id is None and scan_id is not None:
            r = self.store.q1("SELECT study_id FROM scans WHERE id=?", (scan_id,))
            study_id = r["study_id"] if r else None
        return "Scan " + self.blind_code("scan", scan_id, study_id)

    def animal_code(self, specimen_id, study_id=None) -> str:
        if specimen_id is None:
            return "No animal assigned"
        if study_id is None:
            r = self.store.q1("SELECT study_id FROM specimens WHERE id=?", (specimen_id,))
            study_id = r["study_id"] if r else None
        return "Animal " + self.blind_code("animal", specimen_id, study_id)

    def identifying_strings(self, min_len: int = 2) -> list[str]:
        """Strings that identify animals or allocation (file names and stems, paths, animal IDs, group
        names), longest first. Used to mask free text (audit details) in blinded mode."""
        out: set[str] = set()
        for r in self.store.q("SELECT source_name, store_path FROM scans"):
            for v in (r["source_name"], r["store_path"]):
                if v:
                    out.add(str(v))
                    stem = str(v)
                    for suf in (".nii.gz", ".zarr", ".nii", ".npy", ".tif", ".tiff", ".nrrd", ".txm", ".mha", ".mhd"):
                        if stem.lower().endswith(suf):
                            stem = stem[: -len(suf)]
                    out.add(stem)
        for r in self.store.q("SELECT source FROM desktop_import_log"):
            out.add(str(r["source"]))
            out.add(Path(str(r["source"])).name)
        for r in self.store.q("SELECT animal_id FROM specimens"):
            out.add(str(r["animal_id"]))
        for r in self.store.q("SELECT name FROM groups_"):
            out.add(str(r["name"]))
        return sorted((s for s in out if len(s) >= min_len), key=len, reverse=True)

    # ------------------------------------------------------------------ convenience
    def default_store_project(self) -> int:
        u = self.require_user()
        r = self.store.q1("SELECT id FROM projects WHERE org_id=? ORDER BY id LIMIT 1", (u["org_id"],))
        if r:
            return r["id"]
        return self.store.create_project(u, self.name, "Created by OsteoQuant Desktop")

    def create_study(self, name, species="", defect_model="", graft_materials="", blinded=False,
                     data_class="research") -> int:
        """``data_class``: synthetic (phantoms/demo) | public (public dataset) | research (own data) | customer."""
        from ..api.bundle import DATA_CLASSES
        if data_class not in DATA_CLASSES:
            raise ValueError(f"data class must be one of {', '.join(DATA_CLASSES)}")
        return self.store.create_study(self.require_user(), self.default_store_project(), name, species,
                                       defect_model, graft_materials, blinded, data_class=data_class)

    def timepoints(self, study_id) -> list[dict]:
        self.store.study(self.require_user(), study_id)
        return self.store.q("SELECT * FROM timepoints WHERE study_id=? ORDER BY COALESCE(days, 1e9), id", (study_id,))

    def import_log(self, study_id=None) -> list[dict]:
        q = "SELECT * FROM desktop_import_log"
        args = ()
        if study_id is not None:
            q += " WHERE study_id=?"
            args = (study_id,)
        rows = self.store.q(q + " ORDER BY id DESC", args)
        for r in rows:
            r["details"] = json.loads(r["details"] or "{}")
        return rows

    def log_import(self, study_id, source, status, reason="", scan_id=None, details=None):
        u = self.require_user()
        from ..study.db import now
        self.store.exec("INSERT INTO desktop_import_log(study_id,source,status,reason,scan_id,user_id,details,created)"
                        " VALUES (?,?,?,?,?,?,?,?)", (study_id, str(source), status, reason, scan_id, u["id"],
                                                    json.dumps(details or {}, default=str), now()))
        if status == "rejected":
            self.store.audit.record("scan.import_rejected", u["id"], u["org_id"], "study", study_id,
                                    {"source": str(source), "reason": reason})

    def study_tree(self, blinded_view: bool = False) -> list[dict]:
        """Studies -> groups -> animals -> timepoints -> scans, for the project tree.

        Group names follow the store's blinding rules. ``blinded_view`` additionally hides group
        names and animal identifiers for everyone (reviewer blinding in the UI)."""
        u = self.require_user()
        out = []
        for st in self.store.list_studies(u):
            if st.get("status") == "deleted":
                continue
            sid = st["id"]
            groups = {g["id"]: g for g in self.store.groups(u, sid)}
            specs = self.store.specimens(u, sid)
            tps = {t["id"]: t for t in self.timepoints(sid)}
            scans = self.store.scans(u, sid)
            qc = {r["id"]: (json.loads(r["qc"]) if r["qc"] else None)
                  for r in self.store.q("SELECT id, qc FROM scans WHERE study_id=?", (sid,))}
            hidden = blinded_view or bool(st["blinded"]) and not self.can("unblind")
            # study-level blinding is enforced here, whatever the caller asks (C2-PRD-03)
            blinded_view = bool(blinded_view or (st["blinded"] and not self.can("unblind")))

            def scan_node(s):
                q = qc.get(s["id"]) or {}
                return {"kind": "scan", "id": s["id"], "name": s["source_name"] if not blinded_view else self.scan_code(s["id"], sid),
                        "blinded": blinded_view,
                        "status": s["status"], "qc_verdict": q.get("verdict"), "shape": s["shape"],
                        "spacing_um": s["spacing_um"], "timepoint_id": s["timepoint_id"], "specimen_id": s["specimen_id"]}

            def tp_nodes(scan_list):
                by_tp: dict = {}
                for s in scan_list:
                    by_tp.setdefault(s["timepoint_id"], []).append(s)
                nodes = []
                for tid in sorted(by_tp, key=lambda t: (t is None, tps.get(t, {}).get("days") or 0, t or 0)):
                    lbl = tps[tid]["label"] if tid in tps else "No timepoint"
                    nodes.append({"kind": "timepoint", "id": tid, "name": lbl,
                                  "children": [scan_node(s) for s in by_tp[tid]]})
                return nodes

            group_nodes: dict = {}
            for gid, g in groups.items():
                group_nodes[gid] = {"kind": "group", "id": gid, "name": g["blind_code"] if blinded_view else g["name"],
                                    "children": []}
            ungrouped = {"kind": "group", "id": None, "name": "Unassigned group", "children": []}
            for sp in specs:
                ss = [s for s in scans if s["specimen_id"] == sp["id"]]
                node = {"kind": "animal", "id": sp["id"],
                        "name": (self.animal_code(sp["id"], sid) if blinded_view else sp["animal_id"]),
                        "children": tp_nodes(ss)}
                (group_nodes.get(sp["group_id"]) or ungrouped)["children"].append(node)
            orphan = [s for s in scans if s["specimen_id"] is None]
            if orphan:
                ungrouped["children"].append({"kind": "animal", "id": None, "name": "No animal assigned",
                                              "children": tp_nodes(orphan)})
            if blinded_view:     # sort by code so the tree order does not reveal import or allocation order
                for gn in list(group_nodes.values()) + [ungrouped]:
                    gn["children"].sort(key=lambda n: n["name"])
            gnodes = sorted(group_nodes.values(), key=lambda n: n["name"]) if blinded_view else list(group_nodes.values())
            children = gnodes + ([ungrouped] if ungrouped["children"] else [])
            rejected = [r for r in self.import_log(sid) if r["status"] == "rejected"]
            if rejected:
                children.append({"kind": "rejected_folder", "id": sid, "name": f"Rejected imports ({len(rejected)})",
                                 "children": [{"kind": "rejected", "id": r["id"],
                                               "name": f"Rejected import {i + 1}" if blinded_view else Path(r["source"]).name,
                                               "reason": "(hidden in blinded review mode)" if blinded_view else r["reason"],
                                               "status": "rejected"} for i, r in enumerate(rejected)]})
            out.append({"kind": "study", "id": sid, "name": st["name"], "blinded": bool(st["blinded"]),
                        "groups_hidden": hidden, "children": children})
        return out
