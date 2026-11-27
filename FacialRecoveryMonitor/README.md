# Facial Recovery Monitor

**A local, privacy-conscious desktop app for tracking facial movement, symptoms and recovery
progress after facial nerve conditions** — Bell's palsy, facial nerve injury, facial nerve
reconstruction/reanimation, acoustic neuroma surgery and other conditions affecting facial nerve
function. Version 0.9.0 · Research Prototype.

> ⚠️ **Research prototype — not a medical device.** Not clinically validated. It does not diagnose,
> grade severity, rate recovery, predict outcomes or recommend treatment. All landmark-based
> numbers are **experimental**. Always follow the advice of your healthcare team.

![Dashboard](docs/screenshots/01_dashboard.png)

## Start in 3 steps

1. **Unzip** `FacialRecoveryMonitor.zip` (e.g. into Documents).
2. **Double-click the launcher for your computer:**
   * Windows → `START_WINDOWS.bat`
   * Mac → right-click `START_MAC.command` → **Open** (first time), then double-click afterwards
   * Linux → `./start_linux.sh`
3. The first run installs everything automatically (Python 3.12 from the bundled official
   installer if needed, then all app components from the bundled offline packages — no internet
   needed on Windows and Apple-silicon Macs). The app then opens.

**Full instructions:** [LAUNCH_GUIDE](LAUNCH_GUIDE.md) · **Every feature explained:**
[FEATURES_GUIDE](FEATURES_GUIDE.md) · Or open **`START_HERE.html`** in your browser.

## What it does

| Area | Highlights |
|---|---|
| **Dashboard** | Real statistics only (check-ins, surveys, last check-in, tracking duration), quick actions, recent activity, latest experimental values or an explicit "none available" message. |
| **Facial Check-In** | Preparation checklist → live webcam with camera selection, status indicators and MediaPipe face-landmark overlay → 5 guided expressions (neutral, smile, eyebrow raise, eye closure, optional pucker) with Back/Next/Skip/Cancel, countdown and explicit capture → summary with experimental metrics, missing measurements (with reasons) and notes → Save. |
| **Symptom Survey** | 15 questions in 5 sections, validation, automatic drafts, confirmation. No scoring or recommendations. |
| **Progress & Analytics** | Activity, experimental movement (right vs left) and symptom-history charts; All/7/30/90-day filters; hover values; never plots missing values as zero. |
| **Check-In History** | Filter, sort, detailed view, delete with confirmation. |
| **Patient Profile** | Optional name, start date, condition (own words), notes. |
| **Settings** | Camera options, CSV/JSON export, delete all data, privacy information, version. |
| **About** | Purpose, audience, computer-vision vision, limitations, disclaimer. |

**Privacy by design:** local SQLite storage, no account, no network calls, camera only on when you
start a check-in, no video recording, still images off by default, export and deletion under your
control.

## What is in this folder

```
FacialRecoveryMonitor/
├── START_HERE.html            ← open in a browser: links to every guide
├── START_WINDOWS.bat          ← one-click install + start (Windows)
├── START_MAC.command          ← one-click install + start (macOS)
├── start_linux.sh             ← install + start (Linux)
├── LAUNCH_GUIDE.html / .md    ← installation & launch guide, troubleshooting
├── FEATURES_GUIDE.html / .md  ← every screen, button and measurement explained
├── README.html / .md          ← this overview
├── installers/                ← official Python 3.12.10 installers (Windows, macOS) + SHA256SUMS
├── offline_packages/          ← all Python packages for Windows x64 and Apple-silicon Macs
├── main.py                    ← application entry point
├── requirements.txt
├── app/                       ← application source code
│   ├── ui.py, theme.py, dialogs.py, icons.py       (window, design system)
│   ├── camera.py, facial_analysis.py, face_topology.py   (webcam + landmarks + metrics)
│   ├── database.py, export.py, survey_definitions.py, charts.py, config.py, utils.py
│   └── pages/  dashboard, checkin, survey, analytics, history, profile, settings, about
├── assets/                    ← face-landmark model (offline), app icon
├── scripts/                   ← demo-data generator, automated UI test
├── tests/                     ← 26 unit tests (pytest)
└── docs/screenshots/
```

## Manual installation (developers / VS Code)

```bash
python3.12 -m venv .venv                     # Windows: py -3.12 -m venv .venv
source .venv/bin/activate                    # Windows: .venv\Scripts\activate
pip install -r requirements.txt              # or offline: --no-index --find-links offline_packages/<platform>
python main.py
```
Tests: `pip install pytest && python -m pytest -q` · UI walkthrough: `python scripts/ui_smoke_test.py`
· Demo data: `python scripts/seed_demo_data.py` then `FRM_DATA_DIR=demo_data python main.py`.

## Technology

Python · CustomTkinter · OpenCV · MediaPipe Face Landmarker (Tasks API; the older
`mp.solutions` API was removed from recent MediaPipe releases, so the current API is used with the
model file bundled for offline use) · Matplotlib · SQLite · NumPy · Pillow.

## Known limitations

Experimental, unvalidated measurements; sensitive to lighting, camera position and head turn; 2-D
webcam cannot fully correct head rotation; landmark model not evaluated on facial palsy; synkinesis
and muscle tone not measured; no encryption at rest; no clinical, regulatory or security
validation.

---
*Face landmark model: MediaPipe Face Landmarker © Google, Apache License 2.0. Bundled Python
installers © Python Software Foundation (PSF License). Bundled packages retain their own
open-source licences.*
