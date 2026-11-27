# Features Guide — Facial Recovery Monitor

A complete tour of every screen, button and measurement in **Facial Recovery Monitor v0.9.0
(Research Prototype)**. To install and start the app, see the [Launch Guide](LAUNCH_GUIDE.md).

> ⚠️ **Important.** This software is a research prototype. It is **not a medical device**, has
> **not been clinically validated**, does **not diagnose** any condition, does **not recommend
> treatment** and does **not replace healthcare professionals**. Landmark-based numbers are
> **experimental**. Always follow the advice of your healthcare team.

*Screenshots show the built-in synthetic demo dataset (note the yellow "DEMO DATA" badge). The
check-in result screenshots use synthetic values for illustration.*

---

## Contents
1. [Who it is for and what it does](#1-who-it-is-for-and-what-it-does)
2. [The main window and navigation](#2-the-main-window-and-navigation)
3. [Dashboard](#3-dashboard)
4. [Facial Check-In](#4-facial-check-in)
5. [The experimental measurements explained](#5-the-experimental-measurements-explained)
6. [Symptom Survey](#6-symptom-survey)
7. [Progress & Analytics](#7-progress--analytics)
8. [Check-In History](#8-check-in-history)
9. [Patient Profile](#9-patient-profile)
10. [Settings](#10-settings)
11. [About](#11-about)
12. [Your data: privacy, storage, export, deletion](#12-your-data-privacy-storage-export-deletion)
13. [Messages and error handling](#13-messages-and-error-handling)
14. [Tips for consistent check-ins](#14-tips-for-consistent-check-ins)
15. [Frequently asked questions](#15-frequently-asked-questions)
16. [Technical reference](#16-technical-reference)

---

## 1. Who it is for and what it does

Facial Recovery Monitor helps people recovering from conditions that affect the facial nerve —
**Bell's palsy, facial nerve injury, facial nerve reconstruction or reanimation, acoustic neuroma
surgery** and similar — to:

* complete **standardised, guided facial check-ins** with a webcam;
* record **symptoms** with a structured survey;
* keep an **organised, dated history** on their own computer;
* review **charts over time** and **export** records to discuss with their clinician.

The long-term idea is that computer vision could make home recordings more consistent and
quantifiable. In this prototype the numbers are demonstrations of what facial landmarks can
capture — not clinical measurements.

---

## 2. The main window and navigation

![Main window](docs/screenshots/01_dashboard.png)

**Sidebar (left, dark navy)** — always visible:

| Element | Function |
|---|---|
| Logo + "Facial Recovery Monitor" | Application identity. |
| **Dashboard** | Overview (start page). |
| **Facial Check-In** | Guided camera session. |
| **Symptom Survey** | 15-question symptom questionnaire. |
| **Progress & Analytics** | Charts over time. |
| **Check-In History** | Browse, inspect and delete records. |
| **Patient Profile** | Optional personal details. |
| **Settings** | Camera, export, deletion, privacy, version. |
| **About** | Purpose, limitations, disclaimer. |
| Teal bar + highlighted button | Shows which page you are on. |
| "Stored on this device only" card | Reminder that data is local; shows the version number. |
| "DEMO DATA" badge | Only shown when the synthetic demo database is open. |

Pages switch inside the same window. The window can be resized; cards rearrange into fewer columns
on smaller windows. Notifications ("Survey saved", "Check-in saved…") appear briefly in the
top-right corner.

**Leaving a page with unfinished work** — the app protects you from losing work:
* leaving an unfinished check-in asks *"Leave this check-in?"* (and turns the camera off);
* leaving an unsaved check-in summary asks *"Leave without saving?"*;
* leaving the survey keeps your answers as a draft automatically.

---

## 3. Dashboard

![Dashboard](docs/screenshots/01_dashboard.png)

**Header (navy banner):** today's date, the app name, a welcome message (uses your display name
from the profile if you set one), a short description, and three **quick-action buttons**:

| Button | Goes to |
|---|---|
| **Start Facial Check-In** | Facial Check-In page |
| **Complete Symptom Survey** | Symptom Survey page |
| **View Progress** | Progress & Analytics page |

**Statistics cards** (calculated from your saved records only — never invented):

| Card | Shows |
|---|---|
| Facial check-ins | Number of saved check-in sessions. |
| Symptom surveys | Number of saved surveys. |
| Most recent check-in | Date, "Today/Yesterday/N days ago" and time; "—" if none. |
| Tracking duration | Days between your first and most recent record (any type), with both dates. |

![Dashboard lower part](docs/screenshots/02_dashboard_lower.png)

**Recent activity:** your five most recent check-ins and surveys with type, date/time and a summary
(e.g. *"4 of 5 expressions captured · 12 experimental metrics"* or *"15 responses recorded"*).
**Click a row** to open that record in Check-In History. *View full history →* opens the History
page. With no records you see a friendly empty state with a *Start Facial Check-In* button.

**Recovery overview:** the latest check-in's experimental right/left values for smile, eyebrow
raise, eye closure and lip pucker, marked **EXPERIMENTAL**, plus a note that they are not validated
clinical measurements. If no measurements exist it says so explicitly. Below it: the date of your
latest symptom survey.

A teal banner at the bottom reminds you that the dashboard does not diagnose, grade or predict
recovery.

---

## 4. Facial Check-In

A check-in has three stages: **prepare → guided expressions → summary**.

### 4.1 Preparation screen

![Check-in preparation](docs/screenshots/03_checkin_prepare.png)

**Before you begin** — six numbered tips: camera at eye level, consistent lighting, keep your face
visible, remove obstructions (hair over brows, glasses, hats), sit comfortably, keep the set-up
consistent between sessions.

**Session setup:**

| Control | Function |
|---|---|
| **Camera** dropdown | Choose which camera to use (Camera 0 is usually the built-in one). |
| **Scan** | Tests camera numbers 0–4 and lists the ones that deliver images. (Only while the camera is off.) |
| **Save a still image of each expression** switch | **Off by default.** When on, one photo per captured expression is kept in memory and written to your data folder **only if you press Save Session**. Images are never uploaded or exported. |
| *What is recorded* | Plain-language summary of what is and is not stored. |
| **Begin check-in** | Starts the session and turns the camera on (this is the only way the camera turns on). |

### 4.2 Guided expressions

![Guided step](docs/screenshots/04_checkin_guided_step.png)

*(The screenshot shows the camera-unavailable state on a computer with no webcam. With a camera
you see a live, mirrored preview with a thin teal face outline and blue key points.)*

**Left: Live camera card**

| Element | Meaning |
|---|---|
| **Camera status pill** | *Camera 0 on* (green), *Starting camera…*, *Camera off* (grey) or *Camera error* (red). |
| **Face pill** | *Face detected* (green), *No face detected* (amber), or *Detection unavailable*. |
| **Recording landmarks** pill (red) | Visible only while measurements are being captured. |
| Live preview | Your camera image. A **3-2-1 countdown** appears in the middle before capture; a **red border** shows while capturing. |
| Camera error / off panel | Explains the problem (e.g. permission denied) with **Try again** / **Turn camera on**. |
| Camera dropdown | Switch camera (restarts the preview). |
| **Turn camera on / off** | Manually control the camera. |
| **Landmark overlay** switch | Show/hide the facial contour drawing. |
| **Mirror view** switch | Show the preview like a mirror (measurements are unaffected). |
| fps | Frames analysed per second. |

**Right: Step panel**

| Element | Function |
|---|---|
| *STEP n OF 5* + progress segments | Blue = current step, teal = captured, grey = skipped. *OPTIONAL* badge on step 5. |
| Expression name, instruction, detail | What to do and how. |
| Status box | *Not captured yet* → *Get ready… 3/2/1* → *Recording landmarks…* → **Expression captured** (with face-detection quality and head-turn angle) or **No face detected** (with advice) or *Skipped*. |
| **Capture expression** / **Recapture expression** | Starts the countdown (3 s) and then records ~1.6 s of landmark measurements (up to 40 frames). A short system sound plays when capture finishes. |
| **Back** | Previous step (captures are kept). |
| **Next** / **Finish** | Next step; enabled after the step is captured or skipped. On the last step it finishes the session. |
| **Skip this movement** / **Skip and finish** | Skip without capturing — use this if a movement is uncomfortable. |
| **Cancel check-in** (top right) | Asks for confirmation, turns the camera off and discards the session. |

**The five standardised expressions**

| # | Expression | Instruction |
|---|---|---|
| 1 | Neutral position | "Relax your facial muscles and look directly at the camera." — the reference for all movements. |
| 2 | Gentle smile | "Give a gentle smile without forcing the movement." |
| 3 | Eyebrow movement | "Raise your eyebrows gently." |
| 4 | Eye closure | "Gently close your eyes." Press Capture first, then close your eyes for about 5 seconds; listen for the alert sound. |
| 5 | Lip pucker (optional) | "Gently pucker your lips as if about to whistle." Skip it if uncomfortable or not relevant. |

**What happens when you press Capture:** a 3-second countdown, then the app analyses each camera
frame for ~1.6 seconds **on your computer**, keeps the *median* of the landmark measurements and
discards the frames. If fewer than 5 frames contained a face, the step is marked *No face
detected* and you can retry or skip. If your head was turned more than 15°, you are warned.

### 4.3 Session summary

![Session summary](docs/screenshots/05_checkin_results.png)

| Section | Contents |
|---|---|
| **Save Session** (top and bottom) | Stores the session. Before this, nothing is saved. After saving, the button becomes **Update notes**. |
| *Experimental prototype* banner | Reminder that values are not a diagnosis, severity rating, recovery score or prognosis. |
| **Session details** | Date and time, duration, expressions captured (n of 5), face detection (frames with a face / frames analysed), still images. |
| **Completed expressions** | Each expression with a status badge: *Captured*, *Skipped*, *No face detected*, *Not analysed*. |
| **Experimental landmark measurements** | Table grouped by movement: Right, Left and L/R similarity (see section 5). |
| **Missing measurements** | Every value that could not be calculated, grouped by reason (e.g. *"Requires a successfully analysed 'Lip pucker' capture"*). **No substitute values are ever used.** |
| **Session notes** (*USER-ENTERED*) | Free text, up to 5,000 characters. |
| **View Progress**, **Return to Dashboard**, **Start a new check-in** | Navigation. Leaving without saving asks for confirmation. |

![Measurement table](docs/screenshots/06_checkin_results_metrics.png)

---

## 5. The experimental measurements explained

The app uses the **MediaPipe Face Landmarker**, which locates **478 points** on the face in each
camera frame. For each captured expression it:

1. **Straightens** the points so the line between the eyes is horizontal (removes head tilt).
2. **Normalises** distances by the **inter-ocular distance (IOD)** — the distance between the
   centres of the two eyes — so sitting closer or further away does not change the values.
3. Takes the **median** across all frames of the capture (robust to blinks and small movements).
4. Compares each movement with your **neutral** capture from the same session.

| Group | Value | How it is calculated | Unit |
|---|---|---|---|
| Resting position | Eye opening — L/R similarity | smaller ÷ larger resting eye opening | ratio (1.00 = equal) |
| | Brow height difference (L − R) | left minus right brow height above each eye line | % IOD |
| | Mouth-corner height difference (L − R) | positive = left corner sits lower | % IOD |
| Smile | Right / Left movement | how much closer each mouth corner moved toward the outer corner of the eye on the same side | % IOD |
| Eyebrow raise | Right / Left movement | increase in brow height compared with rest | % IOD |
| Eye closure | Right / Left closure | reduction of eye opening (lid gap ÷ eye width) compared with rest; 100% ≈ lids meet | % of resting opening |
| Lip pucker | Right / Left movement | how far each mouth corner moved toward the facial midline | % IOD |
| Each movement | **L/R similarity** | smaller side's movement ÷ larger side's movement (1.00 = equal). Only calculated if at least one side moved enough (≥1% IOD, or ≥10% for eye closure). | ratio |

* **Right / Left = your own** right and left side (not the side of the screen).
* **Head pose** (turn, nod, tilt) is estimated and stored as a quality indicator.
* Model "blendshape" scores (e.g. smile, blink) are stored with each expression for future
  research but are not displayed as results.
* **Missing ≠ zero.** If a value cannot be calculated it is reported as missing with the reason,
  never as 0 or a guess.

**Limitations:** values change with lighting, camera height/distance, head turn, glasses, facial
hair and camera quality; a 2-D webcam cannot fully correct head rotation; the landmark model was
not developed or tested specifically on faces with facial palsy; synkinesis and muscle tone are not
measured. The values have **not** been compared with clinical grading systems such as
House-Brackmann, Sunnybrook or eFACE.

---

## 6. Symptom Survey

![Survey](docs/screenshots/07_survey.png)

**15 questions in 5 sections**, each in its own card. Click one answer pill per question (the
chosen answer turns blue). The box at the top right shows *n of 15 answered* with a progress bar.

| # | Section | Question | Answer options |
|---|---|---|---|
| 1 | Eye symptoms | Do you experience eye dryness? | No · Sometimes · Often · Always |
| 2 | | Have you experienced excessive tearing? | No · Sometimes · Often · Always |
| 3 | | Do you experience difficulty closing your eye? | No · Sometimes · Often · Always |
| 4 | | Do you experience discomfort related to your eye? | No · Sometimes · Often · Always |
| 5 | Oral and speech | Do you experience difficulty speaking? | No · Sometimes · Often · Always |
| 6 | | Do you experience difficulty drinking liquids? | No · Sometimes · Often · Always |
| 7 | | Do you notice food collecting on one side of your mouth? | No · Sometimes · Often · Always |
| 8 | Facial movement | Have you noticed involuntary facial movements? | No · Sometimes · Often · Always |
| 9 | | Have you noticed stiffness or tightness in your facial muscles? | No · Sometimes · Often · Always |
| 10 | | Have you noticed changes in facial movement since your last check-in? | No change noticed · More movement · Less movement · Not sure |
| 11 | Daily activities | Have facial symptoms affected eating? | Not at all · A little · Moderately · A lot |
| 12 | | Have facial symptoms affected communication? | Not at all · A little · Moderately · A lot |
| 13 | | Have facial symptoms affected your daily activities? | Not at all · A little · Moderately · A lot |
| 14 | Recovery habits | Have you completed your recommended exercises? | No · Partly · Yes · Not applicable |
| 15 | | Have you followed your recommended eye-care routine, if applicable? | No · Partly · Yes · Not applicable |

**Additional information (optional):** a free-text notes box (up to 5,000 characters, with a
counter).

| Button / behaviour | What it does |
|---|---|
| **Save Survey** | Checks every question is answered. If not, unanswered cards turn red with *"Please choose an answer"*, a red banner lists the question numbers, and the page scrolls to the first one. When complete, saves with the date and time and shows a **Survey saved** confirmation (with *View in History*). |
| **Cancel** | If anything is filled in, asks *"Discard survey answers?"*; then clears the form and returns to the Dashboard. |
| **Automatic draft** | Every answer and note is saved as a draft immediately ("Draft saved automatically"). If you leave the page — or the app closes — your answers are restored next time with a blue *"We restored unsaved answers…"* banner. |

![Survey validation](docs/screenshots/08_survey_validation.png)

The survey **never scores your answers or gives recommendations**. A banner reminds you to contact
your healthcare provider about worrying symptoms, especially eye pain, redness or difficulty
protecting your eye.

---

## 7. Progress & Analytics

**Date filter** (top right): **All time · Last 7 days · Last 30 days · Last 90 days** — applies to
every chart on the page. A summary line shows how many records are in the selected period.
**Hover over any bar or point** to see its exact date and value.

### Check-in activity
![Activity](docs/screenshots/09_analytics_activity.png)

Bars of facial check-ins (blue) and symptom surveys (teal) per day — or per week when the period is
longer than ~6 weeks.

### Experimental facial movement data
![Movement](docs/screenshots/10_analytics_movement.png)

Choose a **Measurement**:
* *Smile / Eyebrow raise / Eye closure / Lip pucker — right vs left movement* (two lines:
  **right = blue circles, left = teal squares**, each labelled at its end);
* any **L/R similarity** (0–1 scale) or **resting difference** value.

Check-ins without that measurement are **left out, not drawn as zero**. Labelled *EXPERIMENTAL ·
not clinically validated*.

### Symptom history
![Symptoms](docs/screenshots/11_analytics_symptoms.png)

Choose any of the 15 survey questions. The vertical axis lists the answer options in order (they
are positions, not scores). Question 10 has no natural order, so its points are not connected.
"Not applicable" answers are not plotted (their number is noted).

Every chart shows a clean empty state (with a shortcut button) when there is nothing to show. The
page never says whether you are improving or getting worse — it shows what was recorded, for you
and your clinician to interpret.

---

## 8. Check-In History

![History](docs/screenshots/12_history_checkin.png)

**Left: record list**

| Control | Function |
|---|---|
| **All activity / Facial check-ins / Symptom surveys** | Filter by type. |
| *n records* | Count for the current filter. |
| **Newest first / Oldest first** | Sort by date. |
| Record rows | Type, date and time, and a summary. Click to select (highlighted in blue). |

**Right: detail panel** for the selected record

* **Facial check-in:** started/completed times, expressions captured, whether landmark detection
  was available, still images; each expression with status, frames with a face and head-turn angle;
  the experimental measurement table; your notes.
* **Symptom survey:** every question and your answer, grouped by section; your notes.

![Survey detail](docs/screenshots/13_history_survey.png)

**Delete** (red, top right of the detail panel): asks *"Delete this … ? This cannot be undone."*
Deleting a check-in also deletes any still images saved with it.

---

## 9. Patient Profile

![Profile](docs/screenshots/14_profile.png)

All fields are optional and stored only on this computer.

| Field | Rules |
|---|---|
| Display name | Up to 60 characters; used in the Dashboard greeting. |
| Date tracking started | `YYYY-MM-DD`; must be a real date and not in the future. **Use today** fills in today's date. |
| Recovery condition or reason for tracking | Pick a suggestion (Bell's palsy, facial nerve injury, reconstruction/reanimation, acoustic neuroma surgery, Ramsay Hunt syndrome, Other) or type your own. Not used to interpret any data. |
| Personal notes | Up to 5,000 characters. |

**Save profile** validates the fields (problems are listed in a red box and the field is outlined
in red). **Revert changes** reloads the saved version. "Last saved" shows when it was saved.
The page reminds you not to enter unnecessary personal information.

---

## 10. Settings

![Settings](docs/screenshots/15_settings.png)

**Camera**

| Setting | Effect |
|---|---|
| Default camera + **Scan for cameras** | Which camera check-ins use. |
| Show live camera preview | Off = camera still runs during check-ins (for measurements) but no video is shown. |
| Show landmark overlay | Draw/hide the face contour on the preview. |
| Mirror preview | Mirror the preview (measurements unaffected). |
| Save still images by default | Pre-selects image saving at the start of each check-in (off recommended). |

**Export your data** — **Export CSV** or **Export JSON** opens a *Save as* dialog. Exports contain
check-in dates, expression status, experimental metrics (labelled as such), survey responses and
notes, and your profile fields. **Face images are never exported.** *Storage location* shows the
data folder; **Open folder** opens it.

![Settings – privacy and deletion](docs/screenshots/16_settings_privacy.png)

**Privacy** — six plain-language points (local storage only, no uploads or network calls, explicit
camera activation, no video recording, you control your data, facial data is sensitive) and a
validation disclaimer.

**Application** — app name, version, Python version, landmark-model status, developer-mode status
and log-file path. **Check face detection** loads the model and reports whether it works.

**Delete stored data** — **Delete all data…** permanently removes all check-ins, measurements,
surveys, drafts and saved still images (camera preferences are kept). Tick **Keep my profile
details** to keep your profile. You must type **DELETE** to confirm.

---

## 11. About

![About](docs/screenshots/17_about.png)

Application name and version, purpose, **who it is for**, the **important disclaimer** (not a
medical device; not clinically validated; does not diagnose; does not recommend treatments; does
not replace healthcare professionals; uses experimental computer-vision calculations), **how
computer vision could support recovery tracking** (standardised capture, objective movement
tracking, longitudinal overview, clinician-ready summaries) and the **current prototype
limitations**.

![About – limitations](docs/screenshots/18_about_lower.png)

---

## 12. Your data: privacy, storage, export, deletion

* **Everything stays on your computer** in a SQLite database. No account, no cloud, no internet
  connection is used by the app. The face model is bundled and runs locally.
* **Camera:** only on during a check-in you started; turns off when you finish, cancel or leave.
* **No video is ever recorded.** By default only numbers derived from landmarks are stored.
* **Still images:** only if you switch them on for a session and press Save Session.

| Operating system | Data folder |
|---|---|
| Windows | `%APPDATA%\FacialRecoveryMonitor\` |
| macOS | `~/Library/Application Support/FacialRecoveryMonitor/` |
| Linux | `~/.local/share/FacialRecoveryMonitor/` |

Inside: `facial_recovery_monitor.sqlite3` (your records), `snapshots/` (only if you saved images),
`logs/app.log` (technical log; no measurements or answers).

**CSV export columns:** `record_type` (profile / facial_checkin / symptom_survey), `record_id`,
`date`, `time`, `section`, `item`, `value`, `unit`, `data_source` (*experimental_measurement*,
*user_entered* or *capture_status*), `notes`. Opens in Excel, Numbers or Google Sheets.
**JSON export** keeps the full nested structure, including per-expression landmark features.

Facial images and facial measurements are sensitive health-related data: protect your computer
account and any exported files (they are not encrypted).

---

## 13. Messages and error handling

The app explains problems in plain language instead of crashing:

| Situation | What you see |
|---|---|
| No camera / camera in use / permission denied | *Camera unavailable* dialog with OS-specific instructions; the preview shows **Try again**. |
| Camera disconnected mid-session | Status changes to *Camera error* with an explanation. |
| No face in view | Amber *No face detected* pill; capture reports *No face detected* with tips. |
| Face model or MediaPipe unavailable | Banner in the check-in camera card; steps can still be completed, measurements are listed as missing. |
| Unanswered survey questions / invalid profile date / text too long | Highlighted fields with a message. |
| Saving fails (e.g. disk full) | *Not saved* dialog; nothing is partially saved; survey answers stay on screen as a draft. |
| Database cannot be opened at start-up | Dialog with the database location and the reason. |
| Missing Python packages or Tkinter | Message explaining exactly what to install. |
| Any unexpected error | *Something went wrong* dialog; your saved records are unaffected; technical details go to the log file (shown on screen only in developer mode, `FRM_DEV=1`). |

---

## 14. Tips for consistent check-ins

* Same place, same time of day, same lighting (face a window or lamp; avoid bright light behind you).
* Camera at eye level, about an arm's length away, face filling a good part of the frame.
* Look straight at the camera; keep your head still and upright.
* Gentle, natural movements — do not force or strain. Skip anything uncomfortable.
* Watch the quality line after each capture (frames with a face, head-turn angle); recapture if
  needed.
* Use session notes to record anything unusual (tired, different camera, new glasses…).

---

## 15. Frequently asked questions

**Does the app tell me whether I am recovering?** No. It records and organises information; your
clinician interprets it.

**Why does a value say "missing"?** It needs a successful neutral capture and the relevant movement,
and a face visible in at least 5 frames. Ratios also need enough movement on at least one side.

**Why did my values change although I feel the same?** Lighting, camera position, distance, head
angle and expression intensity all affect landmark geometry. Keep the set-up consistent and look
at longer-term patterns, together with your clinician.

**Is my face uploaded anywhere?** No. Nothing leaves your computer unless you export a file and
share it yourself.

**Can I use it without a camera?** Yes — the survey, history, analytics and profile work without
one; check-in measurements need a camera.

**Can I edit a saved record?** You can update a check-in's notes right after saving (*Update
notes*). Otherwise records are kept as recorded; you can delete them in History.

---

## 16. Technical reference

| Component | Technology |
|---|---|
| Language | Python 3.10–3.13 (3.12 bundled/recommended) |
| User interface | CustomTkinter (modern Tk widgets), custom design system (`app/theme.py`), icons drawn with Pillow |
| Camera | OpenCV `VideoCapture` on a background thread (DirectShow on Windows, AVFoundation on macOS) |
| Face landmarks | MediaPipe Face Landmarker (Tasks API, 478 landmarks, head-pose matrix, blendshapes), model bundled in `assets/models/` |
| Charts | Matplotlib embedded in Tk, with hover tooltips |
| Storage | SQLite (WAL mode, foreign keys, parameterised queries) |
| Numerical | NumPy |

**Database tables:** `profile` · `checkin_sessions` · `expression_records` (per expression: status,
frame counts, head pose, median landmark features, blendshapes, optional image path) ·
`session_metrics` (derived experimental values) · `symptom_surveys` · `survey_responses` ·
`app_settings`. Child tables cascade on delete. The schema is created automatically on first start
and existing records are never overwritten.

**Source layout:** `main.py` (start-up checks) · `app/ui.py` (window, navigation, error handling) ·
`app/pages/*.py` (one file per page) · `app/camera.py` · `app/facial_analysis.py` ·
`app/database.py` · `app/export.py` · `app/charts.py` · `app/survey_definitions.py` ·
`app/theme.py` · `app/dialogs.py` · `app/icons.py` · `app/config.py` · `app/utils.py`.

**Environment variables:** `FRM_DATA_DIR` (use another data folder, e.g. demo data) · `FRM_DEV=1`
(show technical error details).

**Tests:** `python -m pytest -q` (26 unit tests) · `python scripts/ui_smoke_test.py` (automated walk
through every page; `--fake-camera image.jpg` simulates a webcam for the full
camera → landmarks → metrics → save pipeline).

*Face landmark model: MediaPipe Face Landmarker © Google, Apache License 2.0.*
