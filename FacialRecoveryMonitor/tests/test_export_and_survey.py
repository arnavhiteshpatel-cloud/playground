import csv
import json

from app.database import Database
from app.export import CSV_COLUMNS, export_csv, export_json
from app.survey_definitions import ADHERENCE, CHANGE, FREQUENCY, QUESTIONS
from app.utils import tracking_duration, validate_date


def test_question_set_matches_specification():
    assert len(QUESTIONS) == 15
    assert [q.number for q in QUESTIONS] == list(range(1, 16))
    assert {"No", "Sometimes"} <= set(FREQUENCY.labels)


def test_option_scores():
    assert FREQUENCY.score("No") == 0 and FREQUENCY.score("Always") == 3
    assert CHANGE.score("More movement") is None  # nominal → no ordering
    assert ADHERENCE.score("Not applicable") is None
    assert "Not applicable" not in ADHERENCE.chart_labels


def test_exports(tmp_path):
    db = Database(tmp_path / "e.sqlite3")
    db.save_profile("Alex", "", "", "")
    db.save_checkin({"started_at": "2026-11-01T10:00:00", "completed_at": "2026-11-01T10:03:00",
                     "notes": "note"},
                    [{"step_order": 1, "expression_key": "neutral", "expression_name": "Neutral",
                      "status": "captured", "frames_total": 30, "frames_with_face": 30,
                      "image_path": "/secret/face.jpg"}],
                    [{"key": "smile_lr_ratio", "label": "Smile ratio", "unit": "ratio",
                      "value": 0.9}])
    db.save_survey("2026-11-01T11:00:00", "survey note",
                   [{"question_key": q.key, "question_text": q.text, "category": q.category,
                     "response_label": q.options.labels[0], "response_score": 0}
                    for q in QUESTIONS])
    j = json.loads(export_json(db, tmp_path / "x.json").read_text())
    assert j["raw_images_included"] is False
    assert "face.jpg" not in json.dumps(j)
    assert j["checkin_sessions"][0]["experimental_metrics"][0]["value"] == 0.9
    export_csv(db, tmp_path / "x.csv")
    with (tmp_path / "x.csv").open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    assert tuple(rows[0].keys()) == CSV_COLUMNS
    sources = {r["data_source"] for r in rows}
    assert {"experimental_measurement", "user_entered"} <= sources
    assert sum(r["record_type"] == "symptom_survey" for r in rows) == 16  # 15 answers + notes
    assert "face.jpg" not in (tmp_path / "x.csv").read_text(encoding="utf-8-sig")
    db.close()


def test_date_validation_and_duration():
    assert validate_date("")[0]
    assert validate_date("2024-02-29")[0]
    assert not validate_date("2024-13-01")[0]
    assert not validate_date("2999-01-01")[0]
    assert tracking_duration(None, None)[0] == "—"
    assert tracking_duration("2026-11-01T10:00:00", "2026-11-01T18:00:00")[0] == "1 day"
    assert tracking_duration("2026-11-01T10:00:00", "2026-11-10T08:00:00")[0] == "10 days"
