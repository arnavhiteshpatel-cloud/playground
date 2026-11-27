"""CSV and JSON export of locally stored records.

Raw face images are never included in exports.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

from .config import APP_NAME, APP_VERSION
from .database import Database, parse_iso
from .facial_analysis import METRIC_BY_KEY

CSV_COLUMNS = ("record_type", "record_id", "date", "time", "section", "item", "value", "unit",
               "data_source", "notes")

DISCLAIMER = ("Exported from a research prototype. Experimental measurements are not clinically "
              "validated and are not a diagnosis.")


def collect_export(db: Database) -> dict:
    sessions = []
    for s in reversed(db.list_checkins()):
        full = db.get_checkin(s["id"]) or {}
        sessions.append({
            "id": full.get("id"),
            "started_at": full.get("started_at"),
            "completed_at": full.get("completed_at"),
            "landmark_detection_available": bool(full.get("landmarks_available")),
            "notes": full.get("notes") or "",
            "expressions": [{
                "step": e["step_order"], "expression": e["expression_name"],
                "status": e["status"], "captured_at": e["captured_at"],
                "frames_analysed": e["frames_total"], "frames_with_face": e["frames_with_face"],
                "head_yaw_deg": e["head_yaw_deg"], "head_pitch_deg": e["head_pitch_deg"],
                "head_roll_deg": e["head_roll_deg"],
                "landmark_features": e["features"],
            } for e in full.get("expressions", [])],
            "experimental_metrics": [{
                "key": m["metric_key"], "label": m["label"], "value": m["value"],
                "unit": m["unit"]} for m in full.get("metrics", [])],
        })
    surveys = []
    for v in reversed(db.list_surveys()):
        full = db.get_survey(v["id"]) or {}
        surveys.append({
            "id": full.get("id"), "completed_at": full.get("completed_at"),
            "notes": full.get("notes") or "",
            "responses": [{"question": r["question_text"], "category": r["category"],
                           "response": r["response_label"]} for r in full.get("responses", [])],
        })
    profile = db.get_profile()
    return {
        "exported_by": f"{APP_NAME} {APP_VERSION}",
        "exported_at": datetime.now().replace(microsecond=0).isoformat(),
        "disclaimer": DISCLAIMER,
        "raw_images_included": False,
        "profile": {k: profile.get(k) for k in ("display_name", "tracking_start_date",
                                                  "condition", "notes")},
        "checkin_sessions": sessions,
        "symptom_surveys": surveys,
    }


def _split(ts: str | None) -> tuple[str, str]:
    dt = parse_iso(ts)
    return (dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")) if dt else ("", "")


def export_json(db: Database, path: Path | str) -> Path:
    path = Path(path)
    path.write_text(json.dumps(collect_export(db), indent=2, ensure_ascii=False),
                    encoding="utf-8")
    return path


def export_csv(db: Database, path: Path | str) -> Path:
    """Write a tidy CSV: one row per recorded item."""
    data = collect_export(db)
    path = Path(path)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_COLUMNS)
        p = data["profile"]
        for item in ("display_name", "tracking_start_date", "condition", "notes"):
            if p.get(item):
                w.writerow(("profile", "", "", "", "Profile", item, p[item], "", "user_entered", ""))
        for s in data["checkin_sessions"]:
            d, t = _split(s["completed_at"])
            w.writerow(("facial_checkin", s["id"], d, t, "Session", "notes", s["notes"], "",
                        "user_entered", ""))
            for e in s["expressions"]:
                quality = (f"{e['frames_with_face']}/{e['frames_analysed']} frames with face"
                           if e["frames_analysed"] else "")
                w.writerow(("facial_checkin", s["id"], d, t, "Expression", e["expression"],
                            e["status"], "", "capture_status", quality))
            for m in s["experimental_metrics"]:
                group = METRIC_BY_KEY[m["key"]].group if m["key"] in METRIC_BY_KEY else ""
                w.writerow(("facial_checkin", s["id"], d, t, f"Experimental metric · {group}",
                            m["label"], round(m["value"], 4), m["unit"],
                            "experimental_measurement", "Not clinically validated"))
        for v in data["symptom_surveys"]:
            d, t = _split(v["completed_at"])
            for r in v["responses"]:
                w.writerow(("symptom_survey", v["id"], d, t, r["category"], r["question"],
                            r["response"], "", "user_entered", ""))
            if v["notes"]:
                w.writerow(("symptom_survey", v["id"], d, t, "Additional information", "notes",
                            v["notes"], "", "user_entered", ""))
    return path
