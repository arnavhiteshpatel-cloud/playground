"""Application-wide constants, paths and runtime flags."""

from __future__ import annotations

import os
import sys
from pathlib import Path

APP_NAME = "Facial Recovery Monitor"
APP_SHORT_NAME = "FacialRecoveryMonitor"
APP_VERSION = "0.9.0"
APP_STAGE = "Research Prototype"
VERSION_LABEL = f"v{APP_VERSION} · {APP_STAGE}"

# Source tree locations -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
MODEL_PATH = ASSETS_DIR / "models" / "face_landmarker.task"
ICON_PNG = ASSETS_DIR / "icon.png"
ICON_ICO = ASSETS_DIR / "icon.ico"

MODEL_DOWNLOAD_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/latest/face_landmarker.task"
)


def _default_data_dir() -> Path:
    """Per-user, per-platform location for the local database and logs."""
    override = os.environ.get("FRM_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()
    home = Path.home()
    if sys.platform.startswith("win"):
        root = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        root = home / "Library" / "Application Support"
    else:
        root = Path(os.environ.get("XDG_DATA_HOME", home / ".local" / "share"))
    return root / APP_SHORT_NAME


DATA_DIR = _default_data_dir()
DB_PATH = DATA_DIR / "facial_recovery_monitor.sqlite3"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
LOG_DIR = DATA_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"

# Developer mode shows technical tracebacks in error dialogs.
DEV_MODE = os.environ.get("FRM_DEV", "").strip() in {"1", "true", "yes"}

IS_WINDOWS = sys.platform.startswith("win")
IS_MAC = sys.platform == "darwin"

# Check-in capture parameters --------------------------------------------------
COUNTDOWN_SECONDS = 3
SAMPLE_SECONDS = 1.6
MAX_SAMPLE_FRAMES = 40
MIN_FACE_FRAMES = 5
HEAD_TURN_WARNING_DEG = 15.0
ANALYSIS_MAX_WIDTH = 640

DISCLAIMER_SHORT = (
    "Prototype software. Not a medical device. Measurements are experimental and "
    "have not been clinically validated."
)
