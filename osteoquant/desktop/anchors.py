"""External anchors for the project audit trail (cycle-3 review C3-PRD-03).

The audit trail inside the project database is a hash chain. It detects edits and deletions, but the application
runs as the user, so anyone who can write the database can also append correctly hashed events or recompute the
whole chain. A local file cannot defend itself against its own writer. The control is to keep copies of the chain
head **outside the project folder** and to print it on every report:

* at report generation, signature and audit export the chain head (sequence number + row hash) is appended to a
  per-user anchor file in the user's configuration directory (never inside the project folder);
* at sign-in every stored anchor of the project is checked; an anchor that no longer matches means the trail was
  rewritten or truncated after that point, and the project refuses electronic signatures until an administrator
  has investigated (the anchor file and the event are named);
* every PDF report prints the chain head it was generated at, so a copy held by the sponsor or QA is an anchor
  the user cannot change.

Residual limitation (stated in docs/user/DATA_PROTECTION.md): a user who can write both the project folder and their
own configuration directory can still rewrite both; only anchors held by someone else (printed reports, exported
audit hashes filed by QA) detect that.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ENV = "OSTEOQUANT_ANCHOR_DIR"


def anchor_dir() -> Path:
    if os.environ.get(ENV):
        return Path(os.environ[ENV])
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
        return base / "OsteoQuant" / "anchors"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "OsteoQuant" / "anchors"
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "osteoquant" / "anchors"


def project_key(store) -> str:
    """Stable identity of a project: the hash of its first audit event (unique per project database)."""
    with store.lock:
        r = store.conn.execute("SELECT row_hash FROM audit_log ORDER BY seq ASC LIMIT 1").fetchone()
    return (r[0] if r else "0" * 64)[:32]


def _file(store) -> Path:
    return anchor_dir() / f"{project_key(store)}.jsonl"


def record_anchor(project, event: str) -> dict:
    """Append the current chain head to the user's anchor file; returns the anchor. Never raises (an anchor that
    cannot be written is reported in the audit trail instead)."""
    store = project.store
    a = store.audit.anchor()
    rec = {"seq": a["seq"], "row_hash": a["row_hash"], "event": event,
           "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "project_folder": str(getattr(project, "folder", ""))}
    try:
        f = _file(store)
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(f, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
    except OSError as e:
        u = getattr(project, "user", None) or {}
        try:
            store.audit.record("audit.anchor_write_failed", u.get("id"), u.get("org_id"), "project", None,
                               {"error": str(e)[:200]})
        except Exception:  # noqa: BLE001
            pass
    return a


def stored_anchors(store) -> list[dict]:
    f = _file(store)
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(line)
            if isinstance(d, dict) and "seq" in d and "row_hash" in d:
                out.append(d)
        except ValueError:
            continue
    return out


def verify_anchors(store) -> list[str]:
    """Problems found (empty list = every stored anchor of this project still matches the trail)."""
    problems = []
    for a in stored_anchors(store):
        try:
            ok = store.audit.verify_anchor({"seq": int(a["seq"]), "row_hash": a["row_hash"]})
        except (TypeError, ValueError, KeyError):
            ok = False
        if not ok:
            problems.append(f"audit trail no longer matches the anchor recorded at {a.get('time', '?')} "
                            f"({a.get('event', '?')}, event {a.get('seq')}): the trail was rewritten or truncated "
                            f"after that point (anchor file {_file(store)})")
    return problems
