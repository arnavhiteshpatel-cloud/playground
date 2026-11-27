import sqlite3

import pytest

from app.database import Database, StorageError
from app.survey_definitions import QUESTIONS


@pytest.fixture()
def db(tmp_path):
    d = Database(tmp_path / "t.sqlite3")
    yield d
    d.close()


def _responses():
    return [{"question_key": q.key, "question_text": q.text, "category": q.category,
             "response_label": q.options.labels[0], "response_score": q.options.score(
                 q.options.labels[0])} for q in QUESTIONS]


def _checkin(db, ts="2026-11-01T10:00:00", metrics=None):
    exprs = [{"step_order": 1, "expression_key": "neutral", "expression_name": "Neutral",
              "status": "captured", "frames_total": 20, "frames_with_face": 20,
              "features": {"eye_open_r": 0.3}},
             {"step_order": 2, "expression_key": "smile", "expression_name": "Smile",
              "status": "skipped"}]
    return db.save_checkin({"started_at": ts, "completed_at": ts, "notes": "hello"}, exprs,
                           metrics or [])


def test_schema_created_and_empty(db):
    s = db.summary()
    assert s["checkin_count"] == 0 and s["survey_count"] == 0
    assert s["first_record"] is None
    assert db.activity() == []


def test_records_persist_across_reopen(tmp_path):
    path = tmp_path / "p.sqlite3"
    d = Database(path)
    _checkin(d)
    d.save_survey("2026-11-02T09:00:00", "n", _responses())
    d.close()
    d2 = Database(path)  # reopening must not wipe anything
    s = d2.summary()
    assert s["checkin_count"] == 1 and s["survey_count"] == 1
    d2.close()


def test_checkin_roundtrip_and_missing_metric_not_stored(db):
    sid = _checkin(db, metrics=[
        {"key": "smile_lr_ratio", "label": "x", "unit": "ratio", "value": 0.8},
        {"key": "brow_lr_ratio", "label": "y", "unit": "ratio", "value": None}])
    data = db.get_checkin(sid)
    assert [e["status"] for e in data["expressions"]] == ["captured", "skipped"]
    assert data["expressions"][0]["features"] == {"eye_open_r": 0.3}
    assert [m["metric_key"] for m in data["metrics"]] == ["smile_lr_ratio"]


def test_delete_cascades(db):
    sid = _checkin(db, metrics=[{"key": "k", "label": "l", "unit": "ratio", "value": 1.0}])
    db.delete_checkin(sid)
    assert db.get_checkin(sid) is None
    assert db.metric_series() == []
    n = db._conn.execute("SELECT COUNT(*) FROM expression_records").fetchone()[0]
    assert n == 0


def test_survey_and_series_and_filters(db):
    db.save_survey("2026-10-01T09:00:00", "", _responses())
    db.save_survey("2026-11-01T09:00:00", "", _responses())
    assert len(db.survey_series("eye_dryness")) == 2
    assert len(db.survey_series("eye_dryness", since="2026-10-15T00:00:00")) == 1
    assert db.activity("checkin") == []
    acts = db.activity("survey", newest_first=False)
    assert acts[0]["timestamp"] < acts[1]["timestamp"]


def test_empty_survey_rejected(db):
    with pytest.raises(StorageError):
        db.save_survey("2026-11-01T09:00:00", "", [])


def test_duplicate_response_rolls_back(db):
    r = _responses()
    with pytest.raises(StorageError):
        db.save_survey("2026-11-01T09:00:00", "", r + [r[0]])
    assert db.summary()["survey_count"] == 0  # atomic: nothing partially saved


def test_profile_and_settings(db):
    db.save_profile("Alex", "2026-01-02", "Bell's palsy", "notes")
    assert db.get_profile()["display_name"] == "Alex"
    db.save_profile("Sam", "", "", "")
    assert db.get_profile()["display_name"] == "Sam"
    db.set_setting("camera_index", 2)
    assert db.get_setting("camera_index") == 2
    assert db.get_setting("missing", "d") == "d"


def test_parameterised_queries_resist_injection(db):
    db.save_profile("x'); DROP TABLE profile; --", "", "", "")
    assert db.get_profile()["display_name"].startswith("x')")


def test_delete_all(db):
    _checkin(db)
    db.save_survey("2026-11-01T09:00:00", "", _responses())
    db.save_profile("A", "", "", "")
    db.set_setting("camera_index", 1)
    db.delete_all_data()
    assert db.summary()["checkin_count"] == 0
    assert db.get_profile()["display_name"] == ""
    assert db.get_setting("camera_index") == 1  # device preferences are kept


def test_unopenable_database_raises_storage_error(tmp_path):
    bad = tmp_path / "dir_not_file"
    bad.mkdir()
    with pytest.raises(StorageError):
        Database(bad)


def test_foreign_keys_enforced(db):
    with pytest.raises(sqlite3.IntegrityError):
        db._conn.execute("INSERT INTO session_metrics(session_id, metric_key, label, value) "
                         "VALUES (999, 'k', 'l', 1)")
