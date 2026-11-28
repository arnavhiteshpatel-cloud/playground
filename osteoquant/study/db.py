"""Study store (SQLite) with organisations, users/roles, studies, groups, specimens, timepoints,
scans, analysis configurations, versioned ROIs and segmentations, measurements, reviews,
background jobs and reports.

Tenant isolation: every top-level object carries ``org_id``; all repository functions take the
acting user and filter by the user's organisation. Cross-organisation access raises
``PermissionError`` (tested in tests/test_api.py).

Blinding: when a study is blinded, users without the ``unblind`` permission see a group code
(e.g. "G-7F3A") instead of the group name. Unblinding is an audited admin action.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from ..audit import AuditLog

SCHEMA_VERSION = 3
MIGRATIONS = {3: """
ALTER TABLE users ADD COLUMN must_change_password INTEGER NOT NULL DEFAULT 0;
""", 2: """
ALTER TABLE reports ADD COLUMN unblinded INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN locked_until REAL DEFAULT 0;
ALTER TABLE reviews ADD COLUMN object_sha256 TEXT;
""", 1: """
CREATE TABLE orgs (id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, created TEXT NOT NULL,
  retention_days INTEGER DEFAULT 3650);
CREATE TABLE users (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL REFERENCES orgs(id),
  username TEXT UNIQUE NOT NULL, full_name TEXT, pw_hash TEXT NOT NULL, role TEXT NOT NULL,
  active INTEGER NOT NULL DEFAULT 1, failed_logins INTEGER NOT NULL DEFAULT 0, created TEXT NOT NULL);
CREATE TABLE sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id),
  created TEXT NOT NULL, expires REAL NOT NULL);
CREATE TABLE projects (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, name TEXT NOT NULL,
  description TEXT, created_by INTEGER, created TEXT NOT NULL);
CREATE TABLE studies (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, project_id INTEGER NOT NULL,
  name TEXT NOT NULL, species TEXT, defect_model TEXT, graft_materials TEXT, blinded INTEGER DEFAULT 0,
  glp INTEGER DEFAULT 0, status TEXT DEFAULT 'open', data_class TEXT DEFAULT 'research', created TEXT NOT NULL);
CREATE TABLE groups_ (id INTEGER PRIMARY KEY, study_id INTEGER NOT NULL, name TEXT NOT NULL,
  description TEXT, blind_code TEXT NOT NULL);
CREATE TABLE specimens (id INTEGER PRIMARY KEY, study_id INTEGER NOT NULL, group_id INTEGER,
  animal_id TEXT NOT NULL, sex TEXT, notes TEXT, UNIQUE(study_id, animal_id));
CREATE TABLE timepoints (id INTEGER PRIMARY KEY, study_id INTEGER NOT NULL, label TEXT NOT NULL, days REAL);
CREATE TABLE scans (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, study_id INTEGER NOT NULL,
  specimen_id INTEGER, timepoint_id INTEGER, store_path TEXT, source_name TEXT, format TEXT,
  file_sha256 TEXT, content_sha256 TEXT, shape TEXT, spacing_um TEXT, meta TEXT, qc TEXT,
  acquisition TEXT, status TEXT DEFAULT 'imported', created_by INTEGER, created TEXT NOT NULL);
CREATE INDEX scans_hash ON scans(org_id, file_sha256);
CREATE TABLE analysis_configs (id INTEGER PRIMARY KEY, study_id INTEGER NOT NULL, name TEXT,
  config TEXT NOT NULL, config_sha256 TEXT NOT NULL, created_by INTEGER, created TEXT NOT NULL);
CREATE TABLE rois (id INTEGER PRIMARY KEY, scan_id INTEGER NOT NULL, version INTEGER NOT NULL,
  definition TEXT NOT NULL, def_sha256 TEXT NOT NULL, method TEXT, confidence REAL,
  created_by INTEGER, reason TEXT, created TEXT NOT NULL, UNIQUE(scan_id, version));
CREATE TABLE segmentations (id INTEGER PRIMARY KEY, scan_id INTEGER NOT NULL, version INTEGER NOT NULL,
  parent_id INTEGER, kind TEXT NOT NULL, method TEXT, model_name TEXT, model_sha256 TEXT,
  roi_id INTEGER, labels_key TEXT, labels_sha256 TEXT, edits TEXT, created_by INTEGER,
  created TEXT NOT NULL, UNIQUE(scan_id, version));
CREATE TABLE measurements (id INTEGER PRIMARY KEY, scan_id INTEGER NOT NULL, segmentation_id INTEGER,
  roi_id INTEGER, config_id INTEGER, metrics TEXT NOT NULL, software_version TEXT, created TEXT NOT NULL);
CREATE TABLE reviews (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, object_type TEXT NOT NULL,
  object_id INTEGER NOT NULL, reviewer_id INTEGER NOT NULL, decision TEXT NOT NULL, meaning TEXT,
  comment TEXT, created TEXT NOT NULL);
CREATE TABLE jobs (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, user_id INTEGER, kind TEXT NOT NULL,
  params TEXT, status TEXT NOT NULL, progress REAL DEFAULT 0, message TEXT, result TEXT,
  cancel_requested INTEGER DEFAULT 0, created TEXT NOT NULL, started TEXT, finished TEXT);
CREATE TABLE reports (id INTEGER PRIMARY KEY, org_id INTEGER NOT NULL, study_id INTEGER NOT NULL,
  pdf_path TEXT, csv_path TEXT, sha256 TEXT, status TEXT, created_by INTEGER, created TEXT NOT NULL);
"""}

ROLES = {
    "admin": {"read", "write", "run", "review", "manage_users", "unblind", "delete", "export"},
    "analyst": {"read", "write", "run", "export"},
    "reviewer": {"read", "review", "export"},
    # reviewer permissions plus unblinding: the study director holds the allocation key of a blinded study
    # and may unblind it (an audited, re-authenticated action). The role is also recorded so that report
    # sign-off can be attributed to the study director (desktop signature rows).
    "study_director": {"read", "review", "export", "unblind"},
    "viewer": {"read"},
}


SELF_APPROVAL_MESSAGES = {
    "segmentation": "Separation of duties: you cannot approve a segmentation you created",
    "report": ("Separation of duties: you cannot approve a report you generated. Another reviewer or the study "
               "director must approve it"),
    "roi": ("Separation of duties: you cannot accept an ROI that you created (or that your analysis run created). "
            "Another reviewer must accept it"),
}


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def hash_password(pw: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    h = hashlib.scrypt(pw.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${h.hex()}"


def check_password(pw: str, stored: str) -> bool:
    try:
        _, s, h = stored.split("$")
        salt = bytes.fromhex(s)
    except (ValueError, AttributeError):   # malformed stored hash -> no match, never a 500 (QA-010)
        return False
    cand = hash_password(pw, salt).split("$")[2]
    return hmac.compare_digest(cand, h)


def password_policy(pw: str):
    if len(pw) < 10 or pw.lower() == pw or not any(c.isdigit() for c in pw):
        raise ValueError("Password must be ≥10 characters with an upper-case letter and a digit")


class Store:
    def __init__(self, path: str | Path, data_dir: str | Path | None = None):
        self.path = str(path)
        self.data_dir = Path(data_dir or Path(self.path).parent / "data")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA foreign_keys=ON")
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.RLock()   # one shared connection: serialise all access (review S-10)
        self.migrate()
        self.audit = AuditLog(self.conn, self.lock)
        # lookups of the audited state of one object (user role checks at sign-in); an index does not
        # change the hash chain
        self.conn.execute("CREATE INDEX IF NOT EXISTS audit_object ON audit_log(object_type, object_id)")

    # ------------------------------------------------------------------ infra
    def migrate(self):
        self.conn.execute("CREATE TABLE IF NOT EXISTS schema_version (v INTEGER)")
        r = self.conn.execute("SELECT max(v) FROM schema_version").fetchone()[0] or 0
        known = max(MIGRATIONS) if MIGRATIONS else 0
        if r > known:
            # cycle-3 review C3-PRD-21: an older application must not open (and silently ignore the newer controls
            # of) a database written by a newer one
            raise RuntimeError(f"This project database has schema version {r}; this OsteoQuant supports up to "
                               f"{known}. Open it with the newer OsteoQuant version that created it.")
        for v in sorted(MIGRATIONS):
            if v > r:
                self.conn.executescript(MIGRATIONS[v])
                self.conn.execute("INSERT INTO schema_version VALUES (?)", (v,))

    def close(self) -> None:
        """Close the shared connection once no other thread is inside a store call (closing a SQLite connection while
        another thread is stepping a statement can crash the interpreter; seen on macOS CI, DF-043)."""
        with self.lock:
            self.conn.close()

    def q(self, sql, args=()):
        with self.lock:
            return [dict(r) for r in self.conn.execute(sql, args).fetchall()]

    def q1(self, sql, args=()):
        with self.lock:
            r = self.conn.execute(sql, args).fetchone()
            return dict(r) if r else None

    def exec(self, sql, args=()) -> int:
        with self.lock:
            cur = self.conn.execute(sql, args)
            return cur.lastrowid

    @contextmanager
    def transaction(self, immediate: bool = True):
        """One SQLite transaction under the store lock. ``immediate`` takes the write lock at once
        (``BEGIN IMMEDIATE``; also serialises against other processes); ``immediate=False`` gives a
        consistent read snapshot. Nested use joins the outer transaction. Audit events recorded inside
        commit or roll back with it."""
        with self.lock:
            if self.conn.in_transaction:
                yield self.conn
                return
            self.conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
            try:
                yield self.conn
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise
            self.conn.execute("COMMIT")

    def snapshot(self):
        """Consistent read snapshot (one read transaction) for multi-query reads such as a report bundle."""
        return self.transaction(immediate=False)

    def _next_version_insert(self, table: str, scan_id, insert_sql: str, args_fn, retries: int = 5):
        """Allocate ``max(version)+1`` and insert in ONE write transaction; the UNIQUE(scan_id, version)
        constraint is the backstop and a collision (another process) is retried (C2-PRD-11)."""
        for attempt in range(retries):
            try:
                with self.transaction():
                    v = (self.conn.execute(f"SELECT max(version) FROM {table} WHERE scan_id=?",
                                           (scan_id,)).fetchone()[0] or 0) + 1
                    rid = self.conn.execute(insert_sql, args_fn(v)).lastrowid
                    return rid, v
            except sqlite3.IntegrityError:
                if attempt == retries - 1 or self.conn.in_transaction:
                    raise
                time.sleep(0.01 * (attempt + 1))
        raise RuntimeError("version allocation failed")

    def backup(self, dest) -> dict:
        """Online consistent backup (SQLite backup API) + SHA-256 of the copy."""
        dst = sqlite3.connect(str(dest))
        self.conn.backup(dst)
        dst.close()
        h = hashlib.sha256(Path(dest).read_bytes()).hexdigest()
        self.audit.record("backup", details={"dest": str(dest), "sha256": h})
        return {"path": str(dest), "sha256": h}

    # ------------------------------------------------------------------ auth
    def create_org(self, name, actor=None) -> int:
        oid = self.exec("INSERT INTO orgs(name,created) VALUES (?,?)", (name, now()))
        self.audit.record("org.create", actor and actor["id"], oid, "org", oid, {"name": name})
        return oid

    def create_user(self, org_id, username, password, role, full_name="", actor=None) -> int:
        if role not in ROLES:
            raise ValueError(f"Unknown role {role}")
        if actor is not None:
            self.require(actor, "manage_users", org_id)
        password_policy(password)
        # a password chosen by an administrator must be changed by its owner at first sign-in (C2-PRD-08)
        uid = self.exec("INSERT INTO users(org_id,username,full_name,pw_hash,role,created,must_change_password) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (org_id, username, full_name, hash_password(password), role, now(), int(actor is not None)))
        self.audit.record("user.create", actor and actor["id"], org_id, "user", uid, {"username": username, "role": role})
        return uid

    def set_user_role(self, actor, user_id, role):
        """Audited role change (administrators only; not one's own role). The audit event is the
        reference the role is checked against at sign-in (C2-PRD-09)."""
        if role not in ROLES:
            raise ValueError(f"Unknown role {role}")
        u = self.q1("SELECT * FROM users WHERE id=?", (user_id,))
        if not u:
            raise KeyError("user not found")
        self.require(actor, "manage_users", u["org_id"])
        if int(user_id) == int(actor["id"]):
            raise ValueError("You cannot change your own role")
        if u["role"] == role:
            return
        with self.transaction():
            self.exec("UPDATE users SET role=? WHERE id=?", (role, user_id))
            self.audit.record("user.role_change", actor["id"], u["org_id"], "user", user_id,
                              {"username": u["username"], "old_role": u["role"], "new_role": role})

    def change_password(self, user, old_password, new_password):
        """Self-service password change: the current password is re-checked (failures count towards
        the lockout), the policy applies, the new password must differ. Other sessions of the user end;
        the calling session continues. Audited (C2-PRD-08)."""
        if not self.reauthenticate(user, old_password):
            raise PermissionError("Current password incorrect (5 failed attempts lock the account for 15 minutes)")
        password_policy(new_password)
        if new_password == old_password:
            raise ValueError("The new password must differ from the current one")
        with self.transaction():
            self.exec("UPDATE users SET pw_hash=?, must_change_password=0 WHERE id=?",
                      (hash_password(new_password), user["id"]))
            self.audit.record("user.password_change", user["id"], user["org_id"], "user", user["id"],
                              {"username": user["username"]})

    def audited_user_state(self, user_id) -> dict | None:
        """Role and active flag of a user as last recorded in the hash-chained audit trail
        (user.create / user.role_change / user.activate / user.deactivate); None if never recorded.
        A role or active-flag change counts only when its recorded actor was, at that point of the trail, an active
        administrator of the same organisation other than the subject (cycle-3 review C3-PRD-03: an appended
        self-promotion event used to be accepted). The chain is unkeyed, so a determined writer can still forge the
        actor field; external anchors (``desktop/anchors.py``) are the control for that."""
        with self.lock:
            rows = self.conn.execute(
                "SELECT user_id, org_id, action, object_id, details FROM audit_log WHERE object_type='user' AND action IN "
                "('user.create','user.role_change','user.activate','user.deactivate') ORDER BY seq").fetchall()
        states: dict[int, dict] = {}
        for actor, org, action, oid, det in rows:
            try:
                subj = int(oid)
                a = int(actor) if actor not in (None, "") else None
                d = json.loads(det or "{}")
            except (TypeError, ValueError):
                continue
            if action == "user.create":
                if subj not in states:
                    states[subj] = {"role": d.get("role"), "active": True, "org": org}
                continue
            sa = states.get(a) if a is not None else None
            if subj not in states or sa is None or a == subj or not sa["active"] or sa["role"] != "admin" \
                    or str(sa["org"]) != str(states[subj]["org"]):
                continue                     # unauthorised or self-recorded change: ignored
            if action == "user.role_change":
                states[subj]["role"] = d.get("new_role")
            else:
                states[subj]["active"] = action == "user.activate"
        st = states.get(int(user_id))
        return {"role": st["role"], "active": st["active"]} if st else None

    def user_record_problem(self, u: dict) -> str | None:
        """Why the stored role / active flag of ``u`` does not match its audited state (None if it
        matches). Detects role escalation by editing the database outside the application (C2-PRD-09)."""
        st = self.audited_user_state(u["id"])
        if st is None:
            return "no audited creation event for this account"
        if st["role"] != u["role"]:
            return f"role '{u['role']}' differs from the last audited role '{st['role']}'"
        if bool(st["active"]) != bool(u["active"]):
            return "active flag differs from the last audited state"
        return None

    def set_user_active(self, actor, user_id, active: bool):
        u = self.q1("SELECT * FROM users WHERE id=?", (user_id,))
        self.require(actor, "manage_users", u["org_id"])
        with self.transaction():
            self.exec("UPDATE users SET active=? WHERE id=?", (int(active), user_id))
            if not active:   # S-20: deactivation ends existing sessions immediately
                self.exec("DELETE FROM sessions WHERE user_id=?", (user_id,))
            self.audit.record("user.activate" if active else "user.deactivate", actor["id"], u["org_id"], "user", user_id)

    def reset_password(self, actor, user_id, new_password):
        """Administrator password reset: policy-checked, clears the lockout, ends sessions, audited."""
        u = self.q1("SELECT * FROM users WHERE id=?", (user_id,))
        if not u:
            raise KeyError("user not found")
        self.require(actor, "manage_users", u["org_id"])
        password_policy(new_password)
        self.exec("UPDATE users SET pw_hash=?, failed_logins=0, locked_until=0, must_change_password=1 WHERE id=?",
                  (hash_password(new_password), user_id))
        self.exec("DELETE FROM sessions WHERE user_id=?", (user_id,))
        self.audit.record("user.password_reset", actor["id"], u["org_id"], "user", user_id, {"username": u["username"]})

    LOCK_SECONDS = 15 * 60
    _DUMMY_HASH = None

    def login(self, username, password, ttl_s=8 * 3600) -> str | None:
        u = self.q1("SELECT * FROM users WHERE username=?", (username,))
        if Store._DUMMY_HASH is None:
            Store._DUMMY_HASH = hash_password("timing-equaliser-Aa1")
        locked = bool(u) and (u.get("locked_until") or 0) > time.time()
        ok = check_password(password, u["pw_hash"] if u else Store._DUMMY_HASH)   # same cost for unknown users
        if not u or not u["active"] or locked:
            self.audit.record("auth.login_failed", None, u and u["org_id"], "user", u and u["id"],
                              {"username": username, "reason": "unknown/inactive/temporarily locked"})
            return None
        if not ok:
            with self.lock:
                self.exec("UPDATE users SET failed_logins=failed_logins+1 WHERE id=?", (u["id"],))
                n = self.q1("SELECT failed_logins FROM users WHERE id=?", (u["id"],))["failed_logins"]
                if n >= 5:   # temporary lock (not permanent) limits the denial-of-service impact
                    self.exec("UPDATE users SET locked_until=?, failed_logins=0 WHERE id=?",
                              (time.time() + self.LOCK_SECONDS, u["id"]))
            self.audit.record("auth.login_failed", u["id"], u["org_id"], "user", u["id"],
                              {"reason": "bad password", "locked": n >= 5})
            return None
        problem = self.user_record_problem(u)
        if problem:   # C2-PRD-09: role or active flag edited outside the audited API
            self.audit.record("auth.user_record_mismatch", u["id"], u["org_id"], "user", u["id"],
                              {"username": username, "reason": problem})
            return None
        self.exec("UPDATE users SET failed_logins=0, locked_until=0 WHERE id=?", (u["id"],))
        self.exec("DELETE FROM sessions WHERE expires < ?", (time.time(),))   # S-20: purge expired sessions
        tok = secrets.token_urlsafe(32)
        self.exec("INSERT INTO sessions VALUES (?,?,?,?)",
                  (hashlib.sha256(tok.encode()).hexdigest(), u["id"], now(), time.time() + ttl_s))
        self.audit.record("auth.login", u["id"], u["org_id"], "user", u["id"])
        return tok

    def reauthenticate(self, user, password) -> bool:
        """Re-check the password of an authenticated user (e-signature). Failures count towards the
        same temporary lockout as login, so a stolen session token cannot be used to brute-force
        the password through the signing endpoint (QA-011 / Gen-2 G2-03)."""
        u = self.q1("SELECT * FROM users WHERE id=?", (user["id"],))
        if not u or not u["active"]:
            return False
        if (u.get("locked_until") or 0) > time.time():
            check_password(password, u["pw_hash"])   # equal cost
            self.audit.record("auth.reauth_failed", u["id"], u["org_id"], "user", u["id"], {"reason": "temporarily locked"})
            return False
        if check_password(password, u["pw_hash"]):
            self.exec("UPDATE users SET failed_logins=0 WHERE id=?", (u["id"],))
            return True
        with self.lock:
            self.exec("UPDATE users SET failed_logins=failed_logins+1 WHERE id=?", (u["id"],))
            n = self.q1("SELECT failed_logins FROM users WHERE id=?", (u["id"],))["failed_logins"]
            if n >= 5:
                self.exec("UPDATE users SET locked_until=?, failed_logins=0 WHERE id=?",
                          (time.time() + self.LOCK_SECONDS, u["id"]))
        self.audit.record("auth.reauth_failed", u["id"], u["org_id"], "user", u["id"],
                          {"reason": "bad password", "locked": n >= 5})
        return False

    def user_for_token(self, tok) -> dict | None:
        if not tok:
            return None
        s = self.q1("SELECT * FROM sessions WHERE token_hash=?", (hashlib.sha256(tok.encode()).hexdigest(),))
        if not s or s["expires"] < time.time():
            return None
        u = self.q1("SELECT id,org_id,username,full_name,role,active FROM users WHERE id=?", (s["user_id"],))
        return u if u and u["active"] else None

    def validate_session(self, tok, sliding_ttl_s: float | None = None) -> dict | None:
        """The session's user, re-read from the database (current role, active flag), or None when the
        session has ended (signed out, expired, deactivated, password reset). With ``sliding_ttl_s`` an
        active session's expiry is extended (desktop sessions stay open while in use)."""
        if not tok:
            return None
        th = hashlib.sha256(tok.encode()).hexdigest()
        s = self.q1("SELECT * FROM sessions WHERE token_hash=?", (th,))
        if not s or s["expires"] < time.time():
            return None
        u = self.q1("SELECT id,org_id,username,full_name,role,active,must_change_password FROM users WHERE id=?",
                    (s["user_id"],))
        if not u or not u["active"]:
            return None
        if sliding_ttl_s and s["expires"] - time.time() < sliding_ttl_s / 2:
            self.exec("UPDATE sessions SET expires=? WHERE token_hash=?", (time.time() + sliding_ttl_s, th))
        return u

    def end_other_sessions(self, user_id, keep_token=None):
        keep = hashlib.sha256(keep_token.encode()).hexdigest() if keep_token else ""
        self.exec("DELETE FROM sessions WHERE user_id=? AND token_hash<>?", (user_id, keep))

    def logout(self, tok):
        self.exec("DELETE FROM sessions WHERE token_hash=?", (hashlib.sha256(tok.encode()).hexdigest(),))

    def can(self, user, perm) -> bool:
        return perm in ROLES.get(user["role"], set())

    def require(self, user, perm, org_id=None):
        if not self.can(user, perm):
            self.audit.record("authz.denied", user["id"], user["org_id"], details={"perm": perm})
            raise PermissionError(f"Role '{user['role']}' lacks permission '{perm}'")
        if org_id is not None and int(org_id) != int(user["org_id"]):
            self.audit.record("authz.cross_tenant_denied", user["id"], user["org_id"], details={"target_org": org_id})
            raise PermissionError("Object belongs to another organisation")

    # ------------------------------------------------------------------ studies
    def create_project(self, user, name, description=""):
        self.require(user, "write")
        pid = self.exec("INSERT INTO projects(org_id,name,description,created_by,created) VALUES (?,?,?,?,?)",
                        (user["org_id"], name, description, user["id"], now()))
        self.audit.record("project.create", user["id"], user["org_id"], "project", pid, {"name": name})
        return pid

    def _project(self, user, pid):
        p = self.q1("SELECT * FROM projects WHERE id=?", (pid,))
        if not p:
            raise KeyError("project not found")
        self.require(user, "read", p["org_id"])
        return p

    def create_study(self, user, project_id, name, species="", defect_model="", graft_materials="",
                     blinded=False, glp=False, data_class="research"):
        self.require(user, "write")
        self._project(user, project_id)
        sid = self.exec("INSERT INTO studies(org_id,project_id,name,species,defect_model,graft_materials,blinded,glp,"
                        "data_class,created) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (user["org_id"], project_id, name, species, defect_model, graft_materials, int(blinded),
                         int(glp), data_class, now()))
        self.audit.record("study.create", user["id"], user["org_id"], "study", sid,
                          {"name": name, "blinded": blinded, "glp_flag": glp, "data_class": data_class})
        return sid

    def study(self, user, sid):
        s = self.q1("SELECT * FROM studies WHERE id=?", (sid,))
        if not s:
            raise KeyError("study not found")
        self.require(user, "read", s["org_id"])
        return s

    def list_studies(self, user):
        self.require(user, "read")
        return self.q("SELECT * FROM studies WHERE org_id=? ORDER BY id", (user["org_id"],))

    def add_group(self, user, sid, name, description=""):
        s = self.study(user, sid)
        self.require(user, "write", s["org_id"])
        code = "G-" + secrets.token_hex(2).upper()
        gid = self.exec("INSERT INTO groups_(study_id,name,description,blind_code) VALUES (?,?,?,?)",
                        (sid, name, description, code))
        self.audit.record("group.create", user["id"], s["org_id"], "group", gid, {"study": sid})
        return gid

    def groups(self, user, sid):
        s = self.study(user, sid)
        rows = self.q("SELECT * FROM groups_ WHERE study_id=? ORDER BY id", (sid,))
        if s["blinded"] and not self.can(user, "unblind"):
            for r in rows:
                r["name"] = r["blind_code"]
                r["description"] = "(blinded)"
        return rows

    def unblind(self, user, sid, reason, details: dict | None = None):
        s = self.study(user, sid)
        self.require(user, "unblind", s["org_id"])
        with self.transaction():
            self.exec("UPDATE studies SET blinded=0 WHERE id=?", (sid,))
            self.audit.record("study.unblind", user["id"], s["org_id"], "study", sid, {"reason": reason, **(details or {})})

    def add_specimen(self, user, sid, animal_id, group_id=None, sex=None, notes=""):
        s = self.study(user, sid)
        self.require(user, "write", s["org_id"])
        if group_id is not None and not self.q1("SELECT id FROM groups_ WHERE id=? AND study_id=?", (group_id, sid)):
            self.audit.record("authz.invalid_group_reference", user["id"], user["org_id"], "study", sid, {"group_id": group_id})
            raise PermissionError("Group does not belong to this study")
        xid = self.exec("INSERT INTO specimens(study_id,group_id,animal_id,sex,notes) VALUES (?,?,?,?,?)",
                        (sid, group_id, animal_id, sex, notes))
        self.audit.record("specimen.create", user["id"], s["org_id"], "specimen", xid, {"animal_id": animal_id})
        return xid

    def add_timepoint(self, user, sid, label, days=None):
        s = self.study(user, sid)
        self.require(user, "write", s["org_id"])
        tid = self.exec("INSERT INTO timepoints(study_id,label,days) VALUES (?,?,?)", (sid, label, days))
        self.audit.record("timepoint.create", user["id"], s["org_id"], "timepoint", tid, {"label": label})
        return tid

    def specimens(self, user, sid):
        self.study(user, sid)
        rows = self.q("SELECT s.*, g.name AS group_name, g.blind_code FROM specimens s LEFT JOIN groups_ g "
                      "ON s.group_id=g.id WHERE s.study_id=? ORDER BY s.id", (sid,))
        st = self.study(user, sid)
        if st["blinded"] and not self.can(user, "unblind"):
            for r in rows:
                r["group_name"] = r["blind_code"]
        return rows

    # ------------------------------------------------------------------ scans
    def register_scan(self, user, sid, specimen_id, timepoint_id, store_path, source_name, fmt, file_sha256,
                      content_sha256, shape, spacing, meta, acquisition=None, allow_duplicate=False):
        s = self.study(user, sid)
        self.require(user, "write", s["org_id"])
        if file_sha256 and not allow_duplicate:
            dup = self.q1("SELECT id, study_id FROM scans WHERE org_id=? AND (file_sha256=? OR content_sha256=?)",
                          (s["org_id"], file_sha256, content_sha256))
            if dup:
                self.audit.record("scan.duplicate_rejected", user["id"], s["org_id"], "scan", dup["id"],
                                  {"file_sha256": file_sha256})
                raise ValueError(f"Duplicate of scan {dup['id']} (same hash)")
        scid = self.exec("INSERT INTO scans(org_id,study_id,specimen_id,timepoint_id,store_path,source_name,format,"
                         "file_sha256,content_sha256,shape,spacing_um,meta,acquisition,created_by,created) "
                         "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (s["org_id"], sid, specimen_id, timepoint_id, str(store_path), source_name, fmt, file_sha256,
                          content_sha256, json.dumps(shape), json.dumps(spacing), json.dumps(meta, default=str),
                          json.dumps(acquisition or {}), user["id"], now()))
        self.audit.record("scan.import", user["id"], s["org_id"], "scan", scid,
                          {"file_sha256": file_sha256, "content_sha256": content_sha256, "source": source_name})
        return scid

    def scan(self, user, scan_id):
        r = self.q1("SELECT * FROM scans WHERE id=?", (scan_id,))
        if not r:
            raise KeyError("scan not found")
        self.require(user, "read", r["org_id"])
        for k in ("shape", "spacing_um", "meta", "qc", "acquisition"):
            if r.get(k):
                r[k] = json.loads(r[k])
        return r

    def scans(self, user, sid):
        self.study(user, sid)
        rows = self.q("SELECT id,specimen_id,timepoint_id,source_name,format,shape,spacing_um,status,file_sha256,created "
                      "FROM scans WHERE study_id=? ORDER BY id", (sid,))
        for r in rows:
            r["shape"], r["spacing_um"] = json.loads(r["shape"]), json.loads(r["spacing_um"])
        return rows

    def set_scan_qc(self, user, scan_id, qc):
        sc = self.scan(user, scan_id)
        self.require(user, "write", sc["org_id"])   # QA-012: writes need write permission
        self.exec("UPDATE scans SET qc=?, status=? WHERE id=?", (json.dumps(qc, default=str), "qc_" + qc["verdict"], scan_id))
        self.audit.record("scan.qc", user["id"], sc["org_id"], "scan", scan_id, {"verdict": qc["verdict"]})

    # ------------------------------------------------------------------ ROI / segmentation versions
    def save_roi(self, user, scan_id, roi_dict, reason=""):
        sc = self.scan(user, scan_id)
        self.require(user, "write", sc["org_id"])
        d = dict(roi_dict)
        rid, v = self._next_version_insert(
            "rois", scan_id, "INSERT INTO rois(scan_id,version,definition,def_sha256,method,confidence,created_by,reason,"
            "created) VALUES (?,?,?,?,?,?,?,?,?)",
            lambda v: (scan_id, v, json.dumps(d, default=float), roi_dict.get("definition_sha256", ""),
                       roi_dict.get("method"), roi_dict.get("confidence"), user["id"], reason, now()))
        self.audit.record("roi.save", user["id"], sc["org_id"], "roi", rid,
                          {"scan": scan_id, "version": v, "def_sha256": roi_dict.get("definition_sha256"),
                           "method": roi_dict.get("method"), "reason": reason})
        return rid, v

    def latest_roi(self, user, scan_id):
        self.scan(user, scan_id)
        r = self.q1("SELECT * FROM rois WHERE scan_id=? ORDER BY version DESC LIMIT 1", (scan_id,))
        if r:
            r["definition"] = json.loads(r["definition"])
        return r

    def roi_history(self, user, scan_id):
        self.scan(user, scan_id)
        return self.q("SELECT id,version,def_sha256,method,confidence,created_by,reason,created FROM rois "
                      "WHERE scan_id=? ORDER BY version", (scan_id,))

    def save_segmentation(self, user, scan_id, kind, labels_key, labels_sha256, method="", model_name=None,
                          model_sha256=None, roi_id=None, parent_id=None, edits=None):
        sc = self.scan(user, scan_id)
        self.require(user, "write", sc["org_id"])
        sid, v = self._next_version_insert(
            "segmentations", scan_id,
            "INSERT INTO segmentations(scan_id,version,parent_id,kind,method,model_name,model_sha256,roi_id,"
            "labels_key,labels_sha256,edits,created_by,created) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            lambda v: (scan_id, v, parent_id, kind, method, model_name, model_sha256, roi_id, labels_key,
                       labels_sha256, json.dumps(edits or {}), user["id"], now()))
        self.audit.record("segmentation.save", user["id"], sc["org_id"], "segmentation", sid,
                          {"scan": scan_id, "version": v, "kind": kind, "model": model_name,
                           "model_sha256": model_sha256, "labels_sha256": labels_sha256, "parent": parent_id,
                           "edits": edits or {}})
        return sid, v

    def segmentations(self, user, scan_id):
        self.scan(user, scan_id)
        rows = self.q("SELECT * FROM segmentations WHERE scan_id=? ORDER BY version", (scan_id,))
        for r in rows:
            r["edits"] = json.loads(r["edits"] or "{}")
        return rows

    def save_measurement(self, user, scan_id, seg_id, roi_id, metrics, software_version, config_id=None):
        sc = self.scan(user, scan_id)
        self.require(user, "write", sc["org_id"])   # QA-012
        mid = self.exec("INSERT INTO measurements(scan_id,segmentation_id,roi_id,config_id,metrics,software_version,created)"
                        " VALUES (?,?,?,?,?,?,?)", (scan_id, seg_id, roi_id, config_id,
                                                    json.dumps(metrics, default=float), software_version, now()))
        self.audit.record("measurement.save", user["id"], sc["org_id"], "measurement", mid,
                          {"scan": scan_id, "segmentation": seg_id, "roi": roi_id})
        return mid

    def latest_measurements(self, user, sid):
        self.study(user, sid)
        rows = self.q("""SELECT m.*, s.specimen_id, s.timepoint_id FROM measurements m JOIN scans s ON m.scan_id=s.id
                         WHERE s.study_id=? AND m.id IN (SELECT max(id) FROM measurements GROUP BY scan_id)
                         ORDER BY m.scan_id""", (sid,))
        for r in rows:
            r["metrics"] = json.loads(r["metrics"])
        return rows

    def review(self, user, object_type, object_id, decision, meaning, comment=""):
        """Record a review/sign-off. ``meaning`` states what the signature means (e.g.
        'reviewed segmentation and approve for reporting')."""
        self.require(user, "review")
        if decision not in ("approved", "rejected", "needs_changes"):
            raise ValueError(decision)
        obj_sha = None
        if object_type == "segmentation":
            seg = self.q1("SELECT s.created_by, s.labels_sha256, sc.org_id FROM segmentations s JOIN scans sc ON s.scan_id=sc.id "
                          "WHERE s.id=?", (object_id,))
            if not seg or int(seg["org_id"]) != int(user["org_id"]):
                raise KeyError("segmentation not found")
            obj_sha = seg["labels_sha256"]
        elif object_type == "report":
            seg = self.q1("SELECT created_by, sha256 AS labels_sha256, org_id FROM reports WHERE id=?", (object_id,))
            if not seg or int(seg["org_id"]) != int(user["org_id"]):
                raise KeyError("report not found")
            obj_sha = seg["labels_sha256"]
        elif object_type == "roi":
            seg = self.q1("SELECT r.created_by, r.def_sha256 AS labels_sha256, sc.org_id FROM rois r JOIN scans sc "
                          "ON r.scan_id=sc.id WHERE r.id=?", (object_id,))
            if not seg or int(seg["org_id"]) != int(user["org_id"]):
                raise KeyError("ROI not found")
            obj_sha = seg["labels_sha256"]
        else:
            seg = None
        if seg is not None:   # separation of duties: authors cannot approve their own work
            if seg["created_by"] == user["id"] and decision == "approved":
                self.audit.record("review.self_approval_denied", user["id"], user["org_id"], object_type, object_id)
                raise PermissionError(SELF_APPROVAL_MESSAGES.get(
                    object_type, f"Separation of duties: you cannot approve a {object_type} you created"))
        rid = self.exec("INSERT INTO reviews(org_id,object_type,object_id,reviewer_id,decision,meaning,comment,created,"
                        "object_sha256) VALUES (?,?,?,?,?,?,?,?,?)",
                        (user["org_id"], object_type, object_id, user["id"], decision, meaning, comment, now(), obj_sha))
        self.audit.record("review." + decision, user["id"], user["org_id"], object_type, object_id,
                          {"meaning": meaning, "comment": comment, "reviewer": user["username"], "object_sha256": obj_sha})
        return rid

    def reviews(self, user, object_type, object_id):
        return self.q("SELECT r.*, u.username, u.full_name FROM reviews r JOIN users u ON r.reviewer_id=u.id "
                      "WHERE r.org_id=? AND object_type=? AND object_id=? ORDER BY r.id",
                      (user["org_id"], object_type, object_id))

    # ------------------------------------------------------------------ data export / deletion
    def export_study(self, user, sid) -> dict:
        s = self.study(user, sid)
        self.require(user, "export", s["org_id"])
        out = {"study": s, "groups": self.groups(user, sid), "specimens": self.specimens(user, sid),
               "timepoints": self.q("SELECT * FROM timepoints WHERE study_id=?", (sid,)),
               "scans": self.scans(user, sid), "measurements": self.latest_measurements(user, sid),
               "audit": (self.audit.events(org_id=s["org_id"], limit=100000)
                         if (self.can(user, "review") or self.can(user, "manage_users")) else "omitted: requires reviewer/admin")}
        self.audit.record("study.export", user["id"], s["org_id"], "study", sid)
        return out

    def delete_study_data(self, user, sid, reason):
        """Deletes scan files and study rows; the audit trail is retained (append-only)."""
        s = self.study(user, sid)
        self.require(user, "delete", s["org_id"])
        import shutil
        for sc in self.q("SELECT id, store_path FROM scans WHERE study_id=?", (sid,)):
            if sc["store_path"] and Path(sc["store_path"]).exists():
                shutil.rmtree(sc["store_path"], ignore_errors=True)
            for t in ("rois", "segmentations", "measurements"):
                self.exec(f"DELETE FROM {t} WHERE scan_id=?", (sc["id"],))
        for rp in self.q("SELECT id, pdf_path, csv_path FROM reports WHERE study_id=?", (sid,)):
            for f in (rp["pdf_path"], rp["csv_path"]):
                if f and Path(f).exists():
                    Path(f).unlink()
            self.exec("DELETE FROM reviews WHERE object_type='report' AND object_id=?", (rp["id"],))
        self.exec("DELETE FROM reports WHERE study_id=?", (sid,))
        self.exec("DELETE FROM analysis_configs WHERE study_id=?", (sid,))
        for t in ("scans", "specimens", "timepoints", "groups_"):
            self.exec(f"DELETE FROM {t} WHERE study_id=?", (sid,))
        self.exec("UPDATE studies SET status='deleted' WHERE id=?", (sid,))
        self.audit.record("study.delete_data", user["id"], s["org_id"], "study", sid, {"reason": reason})
