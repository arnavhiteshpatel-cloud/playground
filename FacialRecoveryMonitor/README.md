# Facial Recovery Monitor

**A local, privacy-conscious desktop prototype for tracking facial movement, symptoms and recovery
progress after facial nerve conditions** — Bell's palsy, facial nerve injury, facial nerve
reconstruction/reanimation, acoustic neuroma surgery and other conditions affecting facial nerve
function.

> ⚠️ **Research prototype — not a medical device.** It has not been clinically validated. It does
> not diagnose, grade severity, rate recovery, predict outcomes or recommend treatment. All
> landmark-based numbers are **experimental**. Always follow the advice of your healthcare team.

![Dashboard](docs/screenshots/dashboard.png)

---

## Contents
1. [Features](#features)
2. [Quick start](#quick-start)
3. [Step-by-step setup in VS Code (beginners)](#step-by-step-setup-in-vs-code-beginners)
4. [Using the app](#using-the-app)
5. [How the experimental measurements work](#how-the-experimental-measurements-work)
6. [Privacy and where your data lives](#privacy-and-where-your-data-lives)
7. [Demo data for presentations](#demo-data-for-presentations)
8. [Testing](#testing)
9. [Project structure](#project-structure)
10. [Troubleshooting](#troubleshooting)
11. [Technology notes and deliberate changes](#technology-notes-and-deliberate-changes)
12. [Known limitations](#known-limitations)

---

## Features

| Area | What works |
|---|---|
| **Dashboard** | Welcome header with today's date, real statistics (check-ins, surveys, last check-in, tracking duration), quick actions, five most recent activities, recovery overview of the latest *experimental* values — or an explicit "no measurements available" message. Nothing is fabricated. |
| **Facial Check-In** | Preparation checklist → live webcam with camera selection, on/off, status pills and a MediaPipe landmark overlay → five guided expressions (neutral, gentle smile, eyebrow raise, eye closure, optional lip pucker) with progress bar, Back / Next / Skip / Cancel, 3-second countdown and explicit capture → results with session details, per-expression status, experimental metrics, missing measurements (with reasons) and a notes field → Save Session / View Progress / Return to Dashboard. |
| **Symptom Survey** | 15 questions in 5 categories as clearly separated cards, nuanced answer scales, required-answer validation (highlighted + scroll to first missing), optional notes, **automatic draft saving** (survives navigation and app restarts), cancel with confirmation, save confirmation. No recommendations are generated. |
| **Progress & Analytics** | Check-in activity chart, experimental movement chart (right vs left, or L/R similarity) with selectable measurement, symptom history chart with selectable question; date filters **All / 7 / 30 / 90 days**; hover tooltips; clean empty states. Missing values are never plotted as zero, and nothing is interpreted as improvement or decline. |
| **Check-In History** | Unified list of check-ins and surveys, filter by type, sort by date, detail panel (metrics, answers, notes), delete with confirmation (also removes any saved still images). |
| **Patient Profile** | Optional display name, tracking start date (validated), condition in the user's own words, notes. |
| **Settings** | Camera selection and scan, live-preview toggle, overlay and mirror toggles, default still-image preference (off), **CSV and JSON export**, open data folder, delete all data (type `DELETE` to confirm), privacy information, version and model status. |
| **About** | Purpose, target users, how computer vision could support recovery tracking, limitations and full disclaimer. |
| **Robustness** | Friendly messages for missing dependencies, unavailable camera / denied permission, no face detected, landmark model unavailable, database failures, invalid input, empty data; tracebacks only in developer mode (`FRM_DEV=1`) and in the log file. |

<table>
<tr><td><img src="docs/screenshots/checkin.png" alt="Check-in preparation"></td>
<td><img src="docs/screenshots/survey.png" alt="Symptom survey"></td></tr>
<tr><td><img src="docs/screenshots/analytics.png" alt="Analytics"></td>
<td><img src="docs/screenshots/history.png" alt="History"></td></tr>
</table>

*(Screenshots use the built-in synthetic demo dataset — note the "DEMO DATA" badge.)*

---

## Quick start

For people already comfortable with Python (3.10, 3.11 or **3.12 recommended**):

```bash
cd FacialRecoveryMonitor
python -m venv .venv
# Windows:  .venv\Scripts\activate        macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Step-by-step setup in VS Code (beginners)

### 1. Install Python
* **Windows:** download Python **3.12** from <https://www.python.org/downloads/>. In the installer
  **tick "Add python.exe to PATH"**, then click *Install Now*. Tkinter (needed for the window) is
  included.
* **macOS:** download the Python **3.12** macOS installer from python.org and run it. (The
  python.org build includes a modern Tkinter; Homebrew Python may need `brew install python-tk`.)
* **Linux (Ubuntu/Debian):** `sudo apt install python3 python3-venv python3-tk`

Check it worked — open a terminal (Windows: *Command Prompt* or *PowerShell*; macOS: *Terminal*):

```bash
python --version        # Windows (or:  py --version)
python3 --version       # macOS / Linux
```

> **Why 3.12?** MediaPipe (face landmarks) publishes ready-made packages for the mainstream
> Python versions first. If `pip install` fails on mediapipe with a newer Python, install 3.12
> alongside it and use that for this project.

### 2. Install VS Code and open the project
1. Install VS Code from <https://code.visualstudio.com/>.
2. Open VS Code → **Extensions** (square icon on the left) → install **"Python"** by Microsoft.
3. Unzip `FacialRecoveryMonitor.zip` somewhere easy, e.g. your Documents folder.
4. **File → Open Folder…** → select the `FacialRecoveryMonitor` folder (the one containing
   `main.py`).
5. Open a terminal inside VS Code: **Terminal → New Terminal**.

### 3. Create and activate a virtual environment
A virtual environment keeps this project's packages separate from the rest of your computer.

**Windows (PowerShell — the VS Code default):**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```
If you see *"running scripts is disabled on this system"*, run this once and try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Windows (Command Prompt):**
```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. In VS Code, press **Ctrl+Shift+P** (macOS: **Cmd+Shift+P**)
→ *Python: Select Interpreter* → choose the one that shows `.venv`.

### 4. Install the dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
This downloads CustomTkinter, OpenCV, MediaPipe, Matplotlib, NumPy and Pillow (a few hundred MB;
it can take a few minutes).

### 5. Run the application
```bash
python main.py
```
The window opens on the Dashboard. Every time you come back later, just open the folder in VS Code,
activate the environment (step 3, second line only) and run `python main.py`.

**macOS:** the first time you start a check-in, macOS asks whether *Terminal* / *Visual Studio
Code* may use the camera — click **Allow**. If you clicked *Don't Allow*, see
[Troubleshooting](#troubleshooting).

---

## Using the app

1. **Patient Profile** (optional): add a display name and when you started tracking.
2. **Facial Check-In:** read the preparation tips → *Begin check-in*. The camera turns on and you
   see yourself with a subtle landmark overlay and a **Face detected** indicator. For each
   expression press **Capture expression**: a 3-second countdown lets you get ready, then about
   1.6 seconds of landmark data is recorded (a red frame and *Recording landmarks* pill show when).
   Use **Next**, **Back**, **Skip this movement**, or **Cancel check-in** at any time. You never have
   to perform a movement that is uncomfortable. At the end, review the summary, add notes and
   press **Save Session**. Nothing is stored before you press Save.
3. **Symptom Survey:** answer the 15 questions and save. Answers are drafted automatically if you
   leave mid-way.
4. **Progress & Analytics** and **Check-In History** let you review everything; use
   **Settings → Export** to create a CSV/JSON file to share with your clinician.

---

## How the experimental measurements work

The MediaPipe **Face Landmarker** finds 478 points on the face in every camera frame, locally.
For each captured expression the app:

1. rotates the points so the line between the eyes is horizontal (removes head tilt);
2. divides distances by the **inter-ocular distance (IOD)** — the distance between the eye
   centres — so values don't depend on how close you sit;
3. takes the **median** over all frames in the capture window (robust to blinks);
4. compares each movement with the **neutral** capture.

| Measurement | Definition (per side) | Unit |
|---|---|---|
| Smile — mouth-corner movement | Decrease in distance between mouth corner and outer eye corner, smile vs neutral | % IOD |
| Eyebrow raise | Increase in brow height above the eye-corner line, raise vs neutral | % IOD |
| Eye closure | Reduction in eye opening (lid gap ÷ eye width), closed vs neutral | % of resting opening |
| Lip pucker | Movement of each mouth corner toward the facial midline | % IOD |
| L/R similarity | Smaller side's movement ÷ larger side's movement (1.00 = equal); only when there was enough movement to compare | ratio |
| Resting differences | Eye-opening similarity, brow-height and mouth-corner-height differences at rest | ratio / % IOD |

"Right" and "left" always mean **your own** right and left. Head turn (yaw) is recorded and you are
warned above 15°. If a value can't be calculated (no face, skipped step, no neutral capture, too
little movement) it is listed under **Missing measurements** with the reason — **it is never
replaced by a guess or a zero.** These numbers have **not** been validated against clinical scales
(House-Brackmann, Sunnybrook, eFACE) and must not be interpreted clinically.

---

## Privacy and where your data lives

* **Local only:** a SQLite database on your computer. No account, cloud, analytics or network
  calls. The face model is bundled (`assets/models/face_landmarker.task`) and runs offline.
* **Camera** turns on only after you press *Begin check-in* and turns off when you finish, cancel
  or leave the page. **Video is never recorded.**
* **Still images** are off by default. If you switch them on for a session, one JPEG per captured
  expression is written **only when you press Save Session**, inside the app's data folder. They
  are never exported and are deleted together with their session.
* **Export** (CSV/JSON) and **Delete all data** are under Settings.

| OS | Data folder |
|---|---|
| Windows | `%APPDATA%\FacialRecoveryMonitor\` |
| macOS | `~/Library/Application Support/FacialRecoveryMonitor/` |
| Linux | `~/.local/share/FacialRecoveryMonitor/` |

Set the environment variable `FRM_DATA_DIR` to use a different folder. Logs are in the `logs`
sub-folder.

**Database tables:** `profile`, `checkin_sessions`, `expression_records` (one row per guided
expression, with frame counts, head pose and median landmark features), `session_metrics` (derived
experimental values), `symptom_surveys`, `survey_responses`, `app_settings`. Child tables use
foreign keys with `ON DELETE CASCADE`; all queries are parameterised.

---

## Demo data for presentations

To show the app with realistic-looking history **without touching your own records**:

```bash
python scripts/seed_demo_data.py          # creates ./demo_data with synthetic records
```
Then start the app pointed at that folder:

```bash
# macOS / Linux
FRM_DATA_DIR=demo_data python main.py
# Windows PowerShell
$env:FRM_DATA_DIR="demo_data"; python main.py
# Windows Command Prompt
set FRM_DATA_DIR=demo_data && python main.py
```
A **"DEMO DATA — synthetic records"** badge is shown in the sidebar whenever the demo database is
open. Close the app and run `python main.py` normally to return to your real data.

---

## Testing

```bash
pip install pytest
python -m pytest -q                         # 25 unit tests: database, metrics, export, validation
python scripts/ui_smoke_test.py             # opens every page and exercises key actions
python scripts/ui_smoke_test.py --fake-camera path/to/face_photo.jpg
                                            # full camera → landmarks → metrics → save pipeline
```
The smoke test uses a temporary database and never touches your data. With `--screens folder/`
it also saves screenshots.

---

## Project structure

```
FacialRecoveryMonitor/
├── main.py                    # entry point: dependency checks, logging, database, window
├── requirements.txt
├── README.md
├── app/
│   ├── config.py              # version, paths, capture parameters
│   ├── database.py            # SQLite schema + parameterised data access
│   ├── camera.py              # OpenCV webcam manager (background thread, explicit sampling)
│   ├── facial_analysis.py     # MediaPipe wrapper, geometric features, experimental metrics
│   ├── face_topology.py       # landmark contour indices for the overlay
│   ├── survey_definitions.py  # the 15 survey questions and answer scales
│   ├── export.py              # CSV / JSON export (never includes images)
│   ├── charts.py              # Matplotlib styling, charts, hover tooltips
│   ├── theme.py               # design system: palette, fonts, cards, buttons, badges
│   ├── icons.py               # line icons + logo drawn with Pillow
│   ├── dialogs.py             # styled modal dialogs and toasts
│   ├── utils.py               # date formatting, validation, date ranges
│   ├── ui.py                  # main window, sidebar navigation, error handling
│   └── pages/                 # dashboard, checkin, survey, analytics, history,
│                              #   profile, settings, about (+ base classes)
├── assets/
│   ├── models/face_landmarker.task   # MediaPipe model (Apache-2.0), used offline
│   ├── icon.png, icon.ico
├── scripts/
│   ├── seed_demo_data.py      # separate synthetic demo database
│   └── ui_smoke_test.py       # automated UI walkthrough
├── tests/                     # pytest unit tests
└── docs/screenshots/
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognised (Windows) | Use `py` instead of `python`, or reinstall Python with **"Add python.exe to PATH"** ticked. |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once, or use Command Prompt and `.venv\Scripts\activate.bat`. |
| `No matching distribution found for mediapipe` | Your Python version is too new/old for MediaPipe. Install Python 3.12, recreate the environment with `py -3.12 -m venv .venv` (Windows) or `python3.12 -m venv .venv`, and reinstall. The app still opens without MediaPipe, but face detection and measurements are disabled. |
| "Missing dependencies" message | The virtual environment is not active or packages are not installed: activate it and run `pip install -r requirements.txt`. |
| "Tkinter is missing" | Windows/macOS: reinstall Python from python.org. Linux: `sudo apt install python3-tk`. Homebrew: `brew install python-tk@3.12`. |
| **macOS: camera unavailable / black** | System Settings → **Privacy & Security → Camera** → enable **Terminal** or **Visual Studio Code** (whichever you started the app from), then quit and reopen that app. |
| **Windows: camera unavailable** | Settings → **Privacy & security → Camera** → turn on *Camera access* and *Let desktop apps access your camera*. Close Teams/Zoom/other apps that may be using the camera. |
| Wrong camera / external webcam not used | Check-In or Settings → **Scan**, then pick the camera number. |
| "No face detected" | Face a light source, move so your whole face is in frame, remove hats/sunglasses, sit ~arm's length from the camera, and look straight at it. |
| "Face landmark model file is missing" | Download <https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task> and save it as `assets/models/face_landmarker.task`. |
| Linux: `libEGL.so.1` / `libGL.so.1` not found | `sudo apt install libegl1 libgl1 libgles2` |
| Linux: camera permission denied | `sudo usermod -aG video $USER`, then log out and in. |
| Window or text too large/small | CustomTkinter follows your OS display scaling; adjust OS scaling or resize the window (layouts reflow). |
| Something went wrong / unexpected error | Details are written to the log file shown in Settings → Application. Run with `FRM_DEV=1` (PowerShell: `$env:FRM_DEV="1"`) to see technical details in the dialog. |

---

## Technology notes and deliberate changes

* **MediaPipe Tasks API instead of the legacy `mp.solutions.face_mesh`.** Recent MediaPipe
  releases removed the old `solutions` API. The app uses the current **Face Landmarker** task
  (478 landmarks, head-pose matrix and blendshape scores) with the model file bundled so it works
  offline and doesn't download anything at run time.
* **CustomTkinter has no drop-shadows,** so cards use subtle 1-px borders on the soft blue-grey
  background to separate surfaces.
* **Custom answer "pills"** replace CustomTkinter's segmented button in the survey, because the
  segmented button cannot show a clearly different text colour for the selected answer.
* **Charts:** right side = blue circles, left side = teal squares (shape + colour, so identity is
  not colour-only); the teal used in charts is a slightly darker step of the brand teal to keep
  ≥ 3:1 contrast on white.
* **Camera opening happens on the UI thread** (required for camera permission prompts on macOS);
  frame reading and landmark detection run on a background thread.

## Known limitations

* Measurements are experimental and unvalidated; they are affected by lighting, camera position,
  distance, head turn, glasses and facial hair.
* A 2-D webcam cannot fully correct for head rotation.
* The landmark model was not trained or evaluated specifically on faces with facial palsy.
* Synkinesis and muscle tone are not measured; the survey only records the user's own report.
* No user accounts or encryption-at-rest: anyone with access to the computer account can read the
  data folder. Protect your computer account and any exported files.
* Not a medical device; no regulatory, clinical or security validation has been performed.

---

*Face landmark model: MediaPipe Face Landmarker © Google, Apache License 2.0. Built with
CustomTkinter, OpenCV, Matplotlib, NumPy and Pillow.*
