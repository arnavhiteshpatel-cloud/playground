"""Audit-trail integrity: any single-field tamper, deletion or reordering is detected."""
import json
import sqlite3
import threading

import pytest
from hypothesis import given
from hypothesis import strategies as hst

from osteoquant.audit.log import GENESIS, AuditLog, canonical

FIELDS = ["ts", "user_id", "org_id", "action", "object_type", "object_id", "details", "prev_hash", "row_hash"]


def _log(n, conn=None):
    conn = conn or sqlite3.connect(":memory:", isolation_level=None)
    log = AuditLog(conn)
    for i in range(n):
        log.record(f"act.{i % 3}", user_id=i % 4 or None, org_id=1 + i % 2, object_type="scan", object_id=i,
                   details={"i": i, "nested": {"x": [1, 2, i]}, "s": "é✓"})
    return conn, log


def _bypass_triggers(conn):
    conn.execute("DROP TRIGGER audit_no_update")
    conn.execute("DROP TRIGGER audit_no_delete")


def test_empty_and_clean_chain_verifies():
    conn, log = _log(0)
    assert log.verify_chain() == {"ok": True, "n": 0, "head": GENESIS}
    conn, log = _log(7)
    r = log.verify_chain()
    assert r["ok"] and r["n"] == 7 and r["head"] == log.anchor()["row_hash"]


@given(n=hst.integers(1, 12), data=hst.data())
def test_any_single_field_tamper_is_detected(n, data):
    conn, log = _log(n)
    _bypass_triggers(conn)
    seq = data.draw(hst.integers(1, n), label="seq")
    field = data.draw(hst.sampled_from(FIELDS), label="field")
    old = conn.execute(f"SELECT {field} FROM audit_log WHERE seq=?", (seq,)).fetchone()[0]
    new = data.draw(hst.one_of(hst.text(min_size=0, max_size=20), hst.none(),
                               hst.just(json.dumps({"i": -1})), hst.just("0" * 64)), label="new")
    if new is None and field in ("ts", "action", "details", "prev_hash", "row_hash"):   # NOT NULL columns
        new = ""
    if new == old or (new is not None and old is not None and str(new) == str(old)):
        new = (old or "") + "x"
    conn.execute(f"UPDATE audit_log SET {field}=? WHERE seq=?", (new, seq))
    r = log.verify_chain()
    assert not r["ok"]
    assert r["first_bad_seq"] in (seq, seq + 1)


@given(n=hst.integers(2, 10), data=hst.data())
def test_deleting_a_non_tail_row_is_detected(n, data):
    conn, log = _log(n)
    _bypass_triggers(conn)
    seq = data.draw(hst.integers(1, n - 1))
    conn.execute("DELETE FROM audit_log WHERE seq=?", (seq,))
    r = log.verify_chain()
    assert not r["ok"] and "prev_hash" in r["reason"]


def test_tail_truncation_needs_anchor():
    conn, log = _log(5)
    anchor = log.anchor()
    _bypass_triggers(conn)
    conn.execute("DELETE FROM audit_log WHERE seq=5")
    assert log.verify_chain()["ok"]                    # documented limitation without an anchor
    assert not log.verify_chain(anchor)["ok"]


def test_reordering_rows_is_detected():
    conn, log = _log(4)
    _bypass_triggers(conn)
    rows = conn.execute("SELECT * FROM audit_log WHERE seq IN (2,3) ORDER BY seq").fetchall()
    conn.execute("DELETE FROM audit_log WHERE seq IN (2,3)")
    for new_seq, row in zip((2, 3), reversed(rows)):
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?,?,?,?,?,?)", (new_seq,) + tuple(row[1:]))
    assert not log.verify_chain()["ok"]


def test_triggers_block_update_and_delete():
    conn, log = _log(2)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE audit_log SET action='x'")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("DELETE FROM audit_log")


def test_anchor_from_empty_log_verifies():
    # QA-008: an anchor exported before the first event ({seq: 0, GENESIS}) used to fail forever
    conn, log = _log(0)
    a0 = log.anchor()
    assert a0 == {"seq": 0, "row_hash": GENESIS}
    assert log.verify_anchor(a0) and log.verify_chain(a0)["ok"]
    log.record("x")
    assert log.verify_chain(a0)["ok"] and log.verify_chain(log.anchor())["ok"]
    assert not log.verify_anchor({"seq": 0, "row_hash": "f" * 64})
    assert not log.verify_anchor({"seq": 99, "row_hash": GENESIS})


def test_timestamp_is_one_instant(monkeypatch):
    # QA-009: seconds and microseconds came from two different clock reads
    import osteoquant.audit.log as al
    seq = iter([1_700_000_000.999999, 1_700_000_001.000001])
    monkeypatch.setattr(al.time, "time", lambda: next(seq))
    conn, log = _log(0)
    ts = log.record("x")["ts"]
    assert ts == "2023-11-14T22:13:20.999999Z"


def test_rollback_on_insert_failure_keeps_chain_valid():
    conn, log = _log(3)
    with pytest.raises(sqlite3.ProgrammingError):
        log.record("x", details={"bad": object()}, object_type=object())   # sqlite cannot bind object
    assert log.verify_chain()["ok"] and log.verify_chain()["n"] == 3
    assert not conn.in_transaction


def test_record_inside_outer_transaction_does_not_commit_it():
    conn, log = _log(1)
    conn.execute("BEGIN")
    log.record("inner")
    conn.execute("ROLLBACK")
    assert log.verify_chain()["n"] == 1


def test_concurrent_writers_keep_one_chain(tmp_path):
    db = tmp_path / "a.db"
    c0 = sqlite3.connect(db, isolation_level=None, check_same_thread=False)
    AuditLog(c0)
    errs = []

    def worker(k):
        try:
            c = sqlite3.connect(db, isolation_level=None, timeout=30)
            lg = AuditLog(c)
            for i in range(15):
                lg.record("w", user_id=k, details={"i": i})
            c.close()
        except Exception as e:  # pragma: no cover
            errs.append(e)
    th = [threading.Thread(target=worker, args=(k,)) for k in range(4)]
    [t.start() for t in th]
    [t.join() for t in th]
    assert not errs
    r = AuditLog(c0).verify_chain()
    assert r["ok"] and r["n"] == 60


def test_events_filtering_and_canonical_json():
    conn, log = _log(6)
    ev = log.events(org_id="1", object_type="scan", object_id=2, limit=10)
    assert len(ev) == 1 and ev[0]["details"]["i"] == 2
    assert len(log.events(limit=3)) == 3
    assert canonical({"b": 1, "a": [1, 2]}) == '{"a":[1,2],"b":1}'
