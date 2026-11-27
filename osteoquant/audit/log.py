"""Append-only, hash-chained audit trail (technical control; not by itself Part 11 compliance).

Each event row stores: seq, UTC timestamp, user_id, org_id, action, object type/id, details
(canonical JSON), prev_hash and row_hash = SHA-256(prev_hash || canonical(event fields)).
Rows are only ever INSERTed; SQLite triggers reject UPDATE and DELETE on the table. Anyone who
bypasses the triggers (e.g. edits the file directly) breaks the chain, which ``verify_chain``
detects and localises. An external anchor (``anchor()``: latest seq + hash) can be exported
and stored elsewhere so that truncation of the tail is also detectable.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time

GENESIS = "0" * 64

SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_log (
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  user_id TEXT,
  org_id TEXT,
  action TEXT NOT NULL,
  object_type TEXT,
  object_id TEXT,
  details TEXT NOT NULL,
  prev_hash TEXT NOT NULL,
  row_hash TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit_log
BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
"""


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _row_hash(prev, ts, user, org, action, otype, oid, details):
    payload = canonical([ts, user, org, action, otype, oid, details])
    return hashlib.sha256((prev + payload).encode()).hexdigest()


class AuditLog:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        conn.executescript(SCHEMA)

    def record(self, action: str, user_id=None, org_id=None, object_type=None, object_id=None,
               details: dict | None = None) -> dict:
        details_s = canonical(details or {})
        ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + f".{int(time.time() * 1e6) % 1000000:06d}Z"
        cur = self.conn.execute("SELECT row_hash FROM audit_log ORDER BY seq DESC LIMIT 1")
        r = cur.fetchone()
        prev = r[0] if r else GENESIS
        h = _row_hash(prev, ts, user_id, org_id, action, object_type, object_id, details_s)
        self.conn.execute("INSERT INTO audit_log(ts,user_id,org_id,action,object_type,object_id,details,prev_hash,row_hash)"
                          " VALUES (?,?,?,?,?,?,?,?,?)",
                          (ts, user_id, org_id, action, object_type, str(object_id) if object_id is not None else None,
                           details_s, prev, h))
        self.conn.commit()
        return {"ts": ts, "row_hash": h}

    def verify_chain(self) -> dict:
        prev = GENESIS
        n = 0
        for row in self.conn.execute("SELECT seq,ts,user_id,org_id,action,object_type,object_id,details,prev_hash,row_hash "
                                     "FROM audit_log ORDER BY seq"):
            seq, ts, u, o, a, ot, oid, det, ph, rh = row
            if ph != prev:
                return {"ok": False, "first_bad_seq": seq, "reason": "prev_hash mismatch (row removed or reordered)", "n": n}
            if _row_hash(prev, ts, u, o, a, ot, oid, det) != rh:
                return {"ok": False, "first_bad_seq": seq, "reason": "row content altered", "n": n}
            prev = rh
            n += 1
        return {"ok": True, "n": n, "head": prev}

    def anchor(self) -> dict:
        r = self.conn.execute("SELECT seq,row_hash FROM audit_log ORDER BY seq DESC LIMIT 1").fetchone()
        return {"seq": r[0], "row_hash": r[1]} if r else {"seq": 0, "row_hash": GENESIS}

    def verify_anchor(self, anchor: dict) -> bool:
        r = self.conn.execute("SELECT row_hash FROM audit_log WHERE seq=?", (anchor["seq"],)).fetchone()
        return bool(r and r[0] == anchor["row_hash"])

    def events(self, org_id=None, object_type=None, object_id=None, limit=500):
        q = "SELECT seq,ts,user_id,org_id,action,object_type,object_id,details,row_hash FROM audit_log WHERE 1=1"
        args = []
        if org_id is not None:
            q += " AND org_id=?"
            args.append(org_id)
        if object_type:
            q += " AND object_type=?"
            args.append(object_type)
        if object_id is not None:
            q += " AND object_id=?"
            args.append(str(object_id))
        q += " ORDER BY seq DESC LIMIT ?"
        args.append(limit)
        cols = ["seq", "ts", "user_id", "org_id", "action", "object_type", "object_id", "details", "row_hash"]
        out = []
        for r in self.conn.execute(q, args):
            d = dict(zip(cols, r))
            d["details"] = json.loads(d["details"])
            out.append(d)
        return out
