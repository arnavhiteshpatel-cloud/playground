"""Facial Recovery Monitor — launch with:  python main.py

Checks dependencies, sets up logging and the local database, then opens the app.
Set the environment variable FRM_DEV=1 to show technical details in error dialogs.
"""

from __future__ import annotations

import importlib
import logging
import logging.handlers
import sys

MIN_PYTHON = (3, 9)

REQUIRED = {  # import name -> pip package name
    "customtkinter": "customtkinter",
    "cv2": "opencv-contrib-python",
    "numpy": "numpy",
    "PIL": "pillow",
    "matplotlib": "matplotlib",
}
OPTIONAL = {"mediapipe": "mediapipe"}


def _fatal(title: str, message: str) -> None:
    """Show an error both in the terminal and, if possible, in a basic dialog."""
    print(f"\n{title}\n{'=' * len(title)}\n{message}\n", file=sys.stderr)
    try:
        import tkinter
        from tkinter import messagebox
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:  # noqa: BLE001 - tkinter itself may be the missing piece
        pass
    sys.exit(1)


def check_environment() -> None:
    if sys.version_info < MIN_PYTHON:
        _fatal("Python version too old",
               f"Facial Recovery Monitor needs Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or newer. "
               f"You are running {sys.version.split()[0]}.")
    try:
        import tkinter  # noqa: F401
    except ImportError:
        _fatal("Tkinter is missing",
               "Your Python installation does not include Tkinter (the window toolkit).\n"
               "• Windows/macOS: reinstall Python from python.org (Tkinter is included).\n"
               "• Linux: install it, e.g.  sudo apt install python3-tk")
    missing = []
    for module, package in REQUIRED.items():
        try:
            importlib.import_module(module)
        except Exception:  # noqa: BLE001
            missing.append(package)
    if missing:
        _fatal("Missing dependencies",
               "These required packages are not installed:\n  " + ", ".join(missing) +
               "\n\nActivate your virtual environment and run:\n"
               "  pip install -r requirements.txt")


def setup_logging() -> None:
    from app.config import DEV_MODE, LOG_DIR, LOG_FILE
    handlers: list[logging.Handler] = []
    if sys.stderr is not None:  # pythonw (no console) has no stderr
        handlers.append(logging.StreamHandler(sys.stderr))
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"))
    except OSError:
        pass
    logging.basicConfig(level=logging.DEBUG if DEV_MODE else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        handlers=handlers)
    for noisy in ("matplotlib", "PIL"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


def main() -> None:
    check_environment()
    setup_logging()
    log = logging.getLogger("main")
    from app.config import DB_PATH, VERSION_LABEL
    from app.database import Database, StorageError
    log.info("Starting Facial Recovery Monitor %s", VERSION_LABEL)
    for module in OPTIONAL:
        try:
            importlib.import_module(module)
        except Exception as exc:  # noqa: BLE001
            log.warning("Optional dependency %s unavailable (%s); face detection disabled.",
                        module, exc)
    try:
        db = Database(DB_PATH)
    except StorageError as exc:
        _fatal("Database could not be opened", str(exc))
        return
    from app.ui import FacialRecoveryApp
    app = FacialRecoveryApp(db)
    app.mainloop()


if __name__ == "__main__":
    main()
