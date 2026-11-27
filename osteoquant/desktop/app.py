"""Entry point: ``python -m osteoquant.desktop`` or the ``osteoquant-desktop`` launcher.

Options
  --project DIR        open this project at start (sign-in dialog follows)
  --theme light|dark   override the saved theme
  --selftest           headless end-to-end check (phantom -> import -> QC -> analysis -> render ->
                       report); exit code 0 on success, 1 on failure
  --screenshots DIR    write screenshots of the main screens (documentation)
  --version            print the version and exit
"""
from __future__ import annotations

import argparse
import os
import sys


def _ensure_std_streams():
    """Windowed builds start without stdout/stderr; give them a sink so library prints and
    warnings cannot raise."""
    for name in ("stdout", "stderr"):
        if getattr(sys, name) is None:
            setattr(sys, name, open(os.devnull, "w", encoding="utf-8"))


def _install_excepthook():
    """Unhandled exceptions in GUI callbacks: log to the user config folder and show a dialog
    instead of failing silently."""
    import traceback

    def hook(etype, value, tb):
        text = "".join(traceback.format_exception(etype, value, tb))
        try:
            from ..licensing import user_config_dir
            d = user_config_dir()
            d.mkdir(parents=True, exist_ok=True)
            with open(d / "error.log", "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError:
            pass
        sys.__stderr__ and sys.__stderr__.write(text)
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox
            if QApplication.instance() is not None:
                box = QMessageBox(QMessageBox.Critical, "Unexpected error",
                                  f"{etype.__name__}: {value}\n\nThe action was not completed. Details were written to "
                                  "error.log in the OsteoQuant settings folder.")
                box.setDetailedText(text)
                box.exec()
        except Exception:  # noqa: BLE001
            pass
    sys.excepthook = hook


def _prepare_environment(headless: bool):
    if headless and "QT_QPA_PLATFORM" not in os.environ:
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
    os.environ.setdefault("MPLBACKEND", "Agg")
    # high-DPI: crisp text and images on scaled displays
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")


def make_app(argv=None):
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    app = QApplication.instance()
    if app is None:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        app = QApplication(argv or [sys.argv[0]])
    app.setApplicationName("OsteoQuant Desktop")
    app.setOrganizationName("OsteoQuant")
    from .. import __version__
    app.setApplicationVersion(__version__)
    from pathlib import Path
    from PySide6.QtGui import QIcon
    icon = Path(__file__).resolve().parent / "resources" / "osteoquant.png"
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))
    return app


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="osteoquant-desktop", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project")
    ap.add_argument("--theme", choices=["light", "dark"])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-out", metavar="DIR", help="keep self-test artefacts and selftest.jsonl in DIR")
    ap.add_argument("--screenshots", metavar="DIR")
    ap.add_argument("--version", action="store_true")
    _ensure_std_streams()
    args, qt_args = ap.parse_known_args(argv)

    if args.version:
        from .. import __version__
        print(f"OsteoQuant Desktop {__version__}")
        return 0
    _prepare_environment(headless=bool(args.selftest or args.screenshots))
    if args.selftest:
        from .selftest import run_selftest
        return run_selftest(out_dir=args.selftest_out)
    app = make_app([sys.argv[0]] + qt_args)
    _install_excepthook()
    from . import theme
    from .settings import AppSettings
    settings = AppSettings()
    theme.apply_theme(app, args.theme or settings.theme)
    if args.screenshots:
        from .screenshots import capture_all
        capture_all(args.screenshots)
        return 0
    from .main_window import MainWindow
    win = MainWindow(settings)
    win.show()
    if args.project:
        win.open_project(args.project)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
