"""Automated UI smoke test: opens every page, exercises key actions, optional screenshots.

Runs against a temporary (or given) data folder, never your real data.

    python scripts/ui_smoke_test.py                      # temporary empty database
    python scripts/ui_smoke_test.py --data-dir demo_data --screens shots/
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _install_fake_camera(image_path: str) -> None:
    import cv2
    import time
    frame = cv2.imread(image_path)
    if frame is None:
        raise SystemExit(f"Could not read {image_path}")

    class FakeCapture:
        def __init__(self, *a, **k):
            self.open = True
        def isOpened(self):
            return self.open
        def read(self):
            time.sleep(1 / 30)
            return True, frame.copy()
        def set(self, *a):
            return True
        def release(self):
            self.open = False

    cv2.VideoCapture = FakeCapture  # type: ignore[misc]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir")
    ap.add_argument("--screens", help="folder to save screenshots into (Linux/X11 or Windows/macOS)")
    ap.add_argument("--size", default="1440x900")
    ap.add_argument("--fake-camera", metavar="IMAGE",
                    help="simulate a webcam that shows this still image (tests the full "
                         "camera → landmarks → metrics → save pipeline without hardware)")
    args = ap.parse_args()
    os.environ["FRM_DATA_DIR"] = args.data_dir or tempfile.mkdtemp(prefix="frm_smoke_")

    from app.config import DB_PATH
    from app.database import Database
    from app.ui import FacialRecoveryApp
    from app import dialogs

    # Auto-answer modal dialogs so the test can run unattended.
    dialogs.ModalDialog.show = lambda self: (self.destroy(), "ok")[1]  # type: ignore[assignment]

    if args.fake_camera:
        _install_fake_camera(args.fake_camera)

    db = Database(DB_PATH)
    app = FacialRecoveryApp(db)
    app.geometry(f"{args.size}+0+0")
    shots = Path(args.screens) if args.screens else None
    if shots:
        shots.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    app.report_callback_exception = lambda et, e, tb: errors.append(  # type: ignore[assignment]
        "".join(traceback.format_exception(et, e, tb)))

    def grab(name: str) -> None:
        if not shots:
            return
        app.update()
        from PIL import ImageGrab
        x, y = app.winfo_rootx(), app.winfo_rooty()
        w, h = app.winfo_width(), app.winfo_height()
        kw = {"xdisplay": os.environ.get("DISPLAY")} if sys.platform.startswith("linux") else {}
        ImageGrab.grab(bbox=(x, y, x + w, y + h), **kw).save(shots / f"{name}.png")

    steps = []
    for key in ("dashboard", "survey", "analytics", "history", "profile", "settings", "about",
                "checkin"):
        steps.append((f"page_{key}", lambda k=key: app.navigate(k)))

    def survey_validation():
        app.navigate("survey")
        app.pages["survey"]._save()  # noqa: SLF001 - empty → validation errors shown
    steps.append(("survey_validation", survey_validation))

    def survey_fill_and_save():
        page = app.pages["survey"]
        for q, card in page.cards.items():
            card.choices.set(card.q.options.labels[1], notify=True)
        page.notes.insert("1.0", "Smoke test survey")
        page._save()  # noqa: SLF001
    steps.append(("survey_saved", survey_fill_and_save))

    def analytics_ranges():
        app.navigate("analytics")
        page = app.pages["analytics"]
        for r in ("Last 7 days", "Last 30 days", "Last 90 days", "All time"):
            page.range_var.set(r)
            page.refresh()
    steps.append(("analytics_all", analytics_ranges))

    def analytics_symptom():
        page = app.pages["analytics"]
        from app.pages.analytics import METRIC_OPTIONS, SYMPTOM_OPTIONS
        for k in list(METRIC_OPTIONS):
            page.metric_var.set(k)
            page.refresh_metric()
        page.metric_var.set(next(iter(METRIC_OPTIONS)))
        page.refresh_metric()
        page.symptom_var.set(list(SYMPTOM_OPTIONS)[9])
        page.refresh_symptom()
    steps.append(("analytics_symptom", analytics_symptom))

    steps.append(("history", lambda: app.navigate("history")))

    def history_filter():
        page = app.pages["history"]
        page.filter_var.set("Symptom surveys")
        page.refresh_list()
        page.sort_var.set("Oldest first")
        page.refresh_list()
        page.filter_var.set("All activity")
        page.sort_var.set("Newest first")
        page.refresh_list()
    steps.append(("history_filtered", history_filter))

    def profile_invalid():
        app.navigate("profile")
        page = app.pages["profile"]
        page.start.delete(0, "end")
        page.start.insert(0, "2999-01-01")
        page._save()  # noqa: SLF001
    steps.append(("profile_invalid", profile_invalid))

    def checkin_begin():
        app.navigate("checkin")
        app.pages["checkin"]._begin()  # noqa: SLF001 - camera absent in CI → error state shown
    steps.append(("checkin_capture", checkin_begin))

    if args.fake_camera:
        def capture_current():
            app.pages["checkin"]._start_capture()  # noqa: SLF001
        def next_step():
            app.pages["checkin"]._next()  # noqa: SLF001
        for i in range(4):
            steps.append((f"checkin_capture_{i}", capture_current))
            steps.append((f"checkin_wait_{i}", lambda: None))
            steps.append((f"checkin_wait_{i}b", lambda: None))
            steps.append((f"checkin_wait_{i}c", lambda: None))
            steps.append((f"checkin_wait_{i}d", lambda: None))
            steps.append((f"checkin_wait_{i}e", lambda: None))
            steps.append((f"checkin_captured_{i}", lambda: None))
            steps.append((f"checkin_next_{i}", next_step))

    def checkin_skip_all():
        page = app.pages["checkin"]
        for _ in range(5):
            if page.stage == "capture":
                page._skip()  # noqa: SLF001
    steps.append(("checkin_results", checkin_skip_all))

    def checkin_save():
        page = app.pages["checkin"]
        page.notes_box.insert("1.0", "Smoke test session")
        page._save()  # noqa: SLF001
    steps.append(("checkin_saved", checkin_save))
    steps.append(("dashboard_after", lambda: app.navigate("dashboard")))

    def run(i: int = 0) -> None:
        if i >= len(steps):
            app.after(200, app.on_close)
            return
        name, fn = steps[i]
        try:
            fn()
        except Exception:  # noqa: BLE001
            errors.append(f"[{name}]\n{traceback.format_exc()}")
        app.update_idletasks()
        app.after(700, lambda: (grab(f"{i:02d}_{name}"), run(i + 1)))

    app.after(800, run)
    app.mainloop()
    s = Database(DB_PATH).summary()
    print(f"Pages exercised: {len(steps)} steps. Records now: {s}")
    if errors:
        print("\nERRORS:\n" + "\n".join(errors))
        return 1
    print("UI smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
