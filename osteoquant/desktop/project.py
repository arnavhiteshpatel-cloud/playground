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
"""


class ProjectError(RuntimeError):
    pass


def is_project_folder(folder) -> bool:
    return (Path(folder) / MARKER).is_file() and (Path(folder) / DB_NAME).is_file()


class Project:
    def __init__(self, folder):
        self.folder = Path(folder).resolve()
        if not is_project_folder(self.folder):
            raise ProjectError(f"{self.folder} is not an OsteoQuant project folder")
        self.meta = json.loads((self.folder / MARKER).read_text(encoding="utf-8"))
        self.store = Store(self.folder / DB_NAME, self.folder / "data")
        self.store.conn.executescript(DESKTOP_SCHEMA)
        self.user: dict | None = None
        self._token: str | None = None

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
    def login(self, username: str, password: str) -> bool:
        tok = self.store.login(username, password)
        if not tok:
            return False
        self._token = tok
        self.user = self.store.user_for_token(tok)
        return True

    def reauthenticate(self, password: str, object_type=None, object_id=None) -> bool:
        """Re-check the signed-in user's password (used before electronic signatures)."""
        row = self.store.q1("SELECT pw_hash FROM users WHERE id=?", (self.require_user()["id"],))
        ok = bool(row) and check_password(password, row["pw_hash"])
        if not ok:
            self.store.audit.record("review.reauth_failed", self.user["id"], self.user["org_id"], object_type, object_id)
        return ok

    def require_user(self) -> dict:
        if not self.user:
            raise ProjectError("Not signed in")
        return self.user

    def can(self, perm: str) -> bool:
        return bool(self.user) and self.store.can(self.user, perm)

    # ------------------------------------------------------------------ convenience
    def default_store_project(self) -> int:
        u = self.require_user()
        r = self.store.q1("SELECT id FROM projects WHERE org_id=? ORDER BY id LIMIT 1", (u["org_id"],))
        if r:
            return r["id"]
        return self.store.create_project(u, self.name, "Created by OsteoQuant Desktop")

    def create_study(self, name, species="", defect_model="", graft_materials="", blinded=False) -> int:
        return self.store.create_study(self.require_user(), self.default_store_project(), name, species,
                                       defect_model, graft_materials, blinded)

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

            def scan_node(s):
                q = qc.get(s["id"]) or {}
                return {"kind": "scan", "id": s["id"], "name": s["source_name"] if not blinded_view else f"Scan {s['id']:04d}",
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
                        "name": (f"Animal {sp['id']:03d}" if blinded_view else sp["animal_id"]),
                        "children": tp_nodes(ss)}
                (group_nodes.get(sp["group_id"]) or ungrouped)["children"].append(node)
            orphan = [s for s in scans if s["specimen_id"] is None]
            if orphan:
                ungrouped["children"].append({"kind": "animal", "id": None, "name": "No animal assigned",
                                              "children": tp_nodes(orphan)})
            children = list(group_nodes.values()) + ([ungrouped] if ungrouped["children"] else [])
            rejected = [r for r in self.import_log(sid) if r["status"] == "rejected"]
            if rejected:
                children.append({"kind": "rejected_folder", "id": sid, "name": f"Rejected imports ({len(rejected)})",
                                 "children": [{"kind": "rejected", "id": r["id"], "name": Path(r["source"]).name,
                                               "reason": r["reason"], "status": "rejected"} for r in rejected]})
            out.append({"kind": "study", "id": sid, "name": st["name"], "blinded": bool(st["blinded"]),
                        "groups_hidden": hidden, "children": children})
        return out
