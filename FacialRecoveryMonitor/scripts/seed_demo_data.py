"""Create a SEPARATE demonstration database filled with clearly-labelled synthetic records.

Use this for presentations or to explore the interface. It never touches your real
data: it writes to its own folder, and the app shows a "DEMO DATA" badge whenever
that database is open.

    python scripts/seed_demo_data.py                       # creates ./demo_data
    FRM_DATA_DIR=demo_data python main.py                 # macOS/Linux
    set FRM_DATA_DIR=demo_data && python main.py          # Windows (cmd)
    $env:FRM_DATA_DIR="demo_data"; python main.py         # Windows (PowerShell)
"""

from __future__ import annotations

import argparse
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.database import Database  # noqa: E402
from app.facial_analysis import EXPRESSIONS, compute_session_metrics  # noqa: E402
from app.survey_definitions import QUESTIONS  # noqa: E402

NEUTRAL = {"eye_open_r": 0.30, "eye_open_l": 0.27, "brow_r": 0.36, "brow_l": 0.33,
           "corner_canthus_r": 1.32, "corner_canthus_l": 1.36, "corner_lateral_r": 0.42,
           "corner_lateral_l": 0.40, "corner_vertical_r": 1.05, "corner_vertical_l": 1.09,
           "mouth_width": 0.82, "mouth_open": 0.01}


def synthetic_session(progress: float, rng: random.Random) -> dict:
    """Synthetic features where the left side moves less, gradually more over time."""
    def j(v, s=0.008):
        return v + rng.gauss(0, s)
    n = {k: j(v, 0.004) for k, v in NEUTRAL.items()}
    left = 0.25 + 0.6 * progress
    return {
        "neutral": n,
        "smile": {**n, "corner_canthus_r": j(n["corner_canthus_r"] - 0.11),
                  "corner_canthus_l": j(n["corner_canthus_l"] - 0.11 * left)},
        "brow_raise": {**n, "brow_r": j(n["brow_r"] + 0.07),
                       "brow_l": j(n["brow_l"] + 0.07 * left)},
        "eye_closure": {**n, "eye_open_r": abs(j(0.02, 0.01)),
                        "eye_open_l": abs(j(n["eye_open_l"] * (1 - 0.9 * min(1, left + 0.15))))},
        "pucker": None if rng.random() < 0.4 else
        {**n, "corner_lateral_r": j(n["corner_lateral_r"] - 0.08),
         "corner_lateral_l": j(n["corner_lateral_l"] - 0.08 * left)},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--data-dir", default=str(ROOT / "demo_data"))
    ap.add_argument("--days", type=int, default=70)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    folder = Path(args.data_dir)
    db_path = folder / "facial_recovery_monitor.sqlite3"
    if db_path.exists():
        sys.exit(f"{db_path} already exists — delete that folder first to regenerate demo data.")
    rng = random.Random(args.seed)
    db = Database(db_path)
    db.set_setting("demo_dataset", True)
    start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) - timedelta(
        days=args.days)
    db.save_profile("Demo user", start.date().isoformat(), "Bell's palsy (demo)",
                    "Synthetic demonstration profile — not a real person.")
    day = 0
    while day <= args.days:
        t = start + timedelta(days=day, hours=rng.randint(0, 10), minutes=rng.randint(0, 59))
        progress = day / args.days
        feats = synthetic_session(progress, rng)
        metrics, _ = compute_session_metrics(feats)
        exprs = []
        for i, e in enumerate(EXPRESSIONS, start=1):
            f = feats.get(e["key"])
            exprs.append({"step_order": i, "expression_key": e["key"],
                          "expression_name": e["name"],
                          "status": "captured" if f else "skipped",
                          "captured_at": t.isoformat() if f else None,
                          "frames_total": 40 if f else 0, "frames_with_face": 40 if f else 0,
                          "head_yaw_deg": rng.uniform(-6, 6) if f else None,
                          "features": f})
        db.save_checkin({"started_at": (t - timedelta(minutes=3)).isoformat(timespec="seconds"),
                         "completed_at": t.isoformat(timespec="seconds"),
                         "camera_index": 0, "landmarks_available": True,
                         "notes": "Synthetic demo session." if rng.random() < 0.3 else ""},
                        exprs, metrics)
        if rng.random() < 0.75:
            responses = []
            for q in QUESTIONS:
                labels = q.options.labels
                if q.options.ordinal and q.options.key in ("frequency", "impact"):
                    idx = max(0, min(len(labels) - 1,
                                     round((1 - progress) * (len(labels) - 1) + rng.gauss(0, 0.6))))
                else:
                    idx = rng.randrange(len(labels))
                responses.append({"question_key": q.key, "question_text": q.text,
                                  "category": q.category, "response_label": labels[idx],
                                  "response_score": q.options.score(labels[idx])})
            db.save_survey((t + timedelta(minutes=5)).isoformat(timespec="seconds"),
                           "Synthetic demo survey.", responses)
        day += rng.choice((2, 3, 4))
    s = db.summary()
    db.close()
    print(f"Demo database created at {db_path}\n"
          f"{s['checkin_count']} synthetic check-ins, {s['survey_count']} synthetic surveys.")


if __name__ == "__main__":
    main()
