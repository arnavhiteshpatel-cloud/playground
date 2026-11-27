# Launch Guide — Facial Recovery Monitor

This guide takes you from the downloaded ZIP file to a running app. **No GitHub account,
programming knowledge or VS Code is needed** for the one-click method.

> ⚠️ Research prototype — not a medical device. Measurements are experimental and not clinically
> validated.

---

## Contents
1. [What is in the ZIP](#1-what-is-in-the-zip)
2. [System requirements](#2-system-requirements)
3. [Step 1 — Unzip the folder](#3-step-1--unzip-the-folder)
4. [Step 2A — Windows: one-click start](#4-step-2a--windows-one-click-start)
5. [Step 2B — Mac: one-click start](#5-step-2b--mac-one-click-start)
6. [Step 2C — Linux](#6-step-2c--linux)
7. [Step 3 — First time in the app](#7-step-3--first-time-in-the-app)
8. [Starting the app again later](#8-starting-the-app-again-later)
9. [Alternative: run it from VS Code](#9-alternative-run-it-from-vs-code)
10. [Demo mode (synthetic data for presentations)](#10-demo-mode-synthetic-data-for-presentations)
11. [Updating, moving or uninstalling](#11-updating-moving-or-uninstalling)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. What is in the ZIP

| Item | What it is |
|---|---|
| `START_HERE.html` | Opens in your web browser and links to all guides. |
| `START_WINDOWS.bat` | **Double-click on Windows** to install (first time) and start the app. |
| `START_MAC.command` | **Double-click on a Mac** to install (first time) and start the app. |
| `start_linux.sh` | Launcher for Linux. |
| `LAUNCH_GUIDE` (.html / .md) | This guide. |
| `FEATURES_GUIDE` (.html / .md) | Every screen, button and measurement explained. |
| `README` (.html / .md) | Overview of the project. |
| `installers/` | Official **Python 3.12.10** installers from python.org for Windows (64-bit) and macOS (+ checksums). |
| `offline_packages/windows-x64/` | Every Python package the app needs, for Windows — **installs with no internet.** |
| `offline_packages/macos-apple-silicon/` | The same for Macs with M1/M2/M3/M4 chips. |
| `main.py`, `app/`, `assets/` | The application source code and its bundled face-landmark model. |
| `scripts/`, `tests/` | Demo-data generator, automated tests. |
| `docs/screenshots/` | Pictures used by the guides. |

Everything the app needs is included. The only software **not** bundled is optional:
[VS Code](https://code.visualstudio.com/) (only if you want to read or edit the code), and for
**Intel Macs or Linux** the Python packages, which the launcher downloads automatically
(about 200 MB, once).

---

## 2. System requirements

| | Minimum |
|---|---|
| **Windows** | Windows 10 or 11, 64-bit |
| **Mac** | macOS 11 Big Sur or newer (Apple silicon: fully offline; Intel: needs internet on first start) |
| **Linux** | 64-bit distribution with Python 3.10+ and Tkinter |
| Disk space | About 1.5 GB free during installation (≈ 700 MB afterwards) |
| Camera | Any built-in or USB webcam (the app also works without one, but check-ins need it) |
| Internet | **Not required** on Windows and Apple-silicon Macs. The app itself never uses the internet. |

---

## 3. Step 1 — Unzip the folder

1. Find `FacialRecoveryMonitor.zip` in your **Downloads** folder.
2. **Windows:** right-click it → **Extract All…** → choose your **Documents** folder → **Extract**.
   (Do not run the app from inside the ZIP preview — it must be extracted.)
   **Mac:** double-click the ZIP; drag the `FacialRecoveryMonitor` folder into **Documents**.
3. Open the extracted `FacialRecoveryMonitor` folder. You should see `START_HERE.html`,
   `START_WINDOWS.bat`, `START_MAC.command` and the other files listed above.

> Tip: keep the folder somewhere permanent such as Documents. The app's own installation lives
> inside this folder (in a hidden `.venv` folder).

---

## 4. Step 2A — Windows: one-click start

1. Double-click **`START_WINDOWS.bat`**.
2. If Windows shows **"Windows protected your PC"** (SmartScreen): click **More info** →
   **Run anyway**. This appears because the file is not from the Microsoft Store.
3. A black window opens and does the first-time setup:
   * **If Python 3.12 is not installed**, it asks *"Install Python 3.12 now [Y,N]?"* — press
     **Y**. The bundled official installer runs for your user account only (no administrator
     password; a progress bar appears for about a minute).
   * It creates the app's private environment and installs all components **from the bundled
     offline packages** (1–3 minutes).
   * When it says **Setup complete**, the app window opens and the black window closes.
4. Later starts: double-click `START_WINDOWS.bat` again — the app opens within a few seconds.

**Optional – desktop shortcut:** right-click `START_WINDOWS.bat` → **Show more options** →
**Send to → Desktop (create shortcut)**.

---

## 5. Step 2B — Mac: one-click start

1. **Right-click** (or Control-click) **`START_MAC.command`** → **Open** → click **Open** in the
   dialog. (The first time, macOS blocks double-clicking files downloaded from the internet that
   are not from the App Store; right-click → Open is the approved way to allow it.)
   * On newer macOS versions, if there is no *Open* button: open **System Settings → Privacy &
     Security**, scroll down to the message about `START_MAC.command` and click **Open Anyway**.
2. A Terminal window opens and does the first-time setup:
   * **If Python 3.12 is not installed**, the official Python installer opens. Click
     **Continue → Continue → Agree → Install**, enter your Mac password, and wait for *"The
     installation was successful"*. Close the installer, go back to the Terminal window and press
     **Return**.
   * It creates the app's private environment and installs all components (offline on Apple-silicon
     Macs; Intel Macs download them once).
3. The app window opens. **Keep the Terminal window open while you use the app** (closing it
   closes the app).
4. The first time you begin a check-in, macOS asks whether **Terminal** may access the camera —
   click **OK**.
5. Later starts: double-click `START_MAC.command`.

> Which Mac do I have? Apple menu  → **About This Mac**. "Chip: Apple M…" = Apple silicon;
> "Processor: Intel…" = Intel.

---

## 6. Step 2C — Linux

```bash
sudo apt install python3 python3-venv python3-tk libegl1 libgl1    # Ubuntu / Debian
cd ~/Documents/FacialRecoveryMonitor
./start_linux.sh
```
The first run downloads the components (needs internet once). Later runs start immediately.
Camera access may require: `sudo usermod -aG video $USER` (then log out and back in).

---

## 7. Step 3 — First time in the app

1. The app opens on the **Dashboard**. All counts are zero — the app never invents data.
2. (Optional) **Patient Profile** → enter a display name → **Save profile**.
3. **Facial Check-In** → read *Before you begin* → **Begin check-in**. Allow camera access if
   asked. You should see yourself with a thin teal outline on your face and a green
   **Face detected** label.
4. For each movement press **Capture expression**, perform the movement during the 3-second
   countdown, hold it until the check mark appears, then press **Next**.
5. On the summary screen press **Save Session**.
6. Complete a **Symptom Survey**, then look at **Progress & Analytics** and **Check-In History**.

The [Features Guide](FEATURES_GUIDE.md) explains every screen in detail.

---

## 8. Starting the app again later

Double-click the same launcher (`START_WINDOWS.bat` or `START_MAC.command`). Your records are kept
between sessions in your user data folder (see the Features Guide → *Your data*), separate from
the app folder — so updating or re-installing the app does not delete them.

---

## 9. Alternative: run it from VS Code

Use this if you want to look at or change the code.

1. Install Python 3.12 (from `installers/` in this folder; on Windows tick **"Add python.exe to
   PATH"**).
2. Install [VS Code](https://code.visualstudio.com/) and its **Python** extension (Extensions icon
   → search "Python" → Install, by Microsoft).
3. **File → Open Folder…** → select `FacialRecoveryMonitor`.
4. **Terminal → New Terminal**, then:

**Windows (PowerShell):**
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install --no-index --find-links offline_packages\windows-x64 -r requirements.txt
python main.py
```
If PowerShell says scripts are disabled: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`,
then repeat the activate line.

**Mac (Terminal / VS Code terminal):**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links offline_packages/macos-apple-silicon -r requirements.txt
#   Intel Mac or with internet:   pip install -r requirements.txt
python main.py
```
5. In VS Code press **Ctrl+Shift+P** (Mac: **Cmd+Shift+P**) → *Python: Select Interpreter* → pick
   the `.venv` entry, so the ▶ Run button uses it.

If you already ran the one-click launcher, the `.venv` exists — just activate it and run
`python main.py`.

**Running the tests:** `pip install pytest` then `python -m pytest -q` (26 tests) and
`python scripts/ui_smoke_test.py` (opens every page automatically).

---

## 10. Demo mode (synthetic data for presentations)

Creates a **separate** database of clearly labelled synthetic records; your real data is not
touched. With the `.venv` activated (see section 9):

```bash
python scripts/seed_demo_data.py
```
Start the app on the demo data:
```bash
# Mac / Linux
FRM_DATA_DIR=demo_data python main.py
# Windows PowerShell
$env:FRM_DATA_DIR="demo_data"; python main.py
# Windows Command Prompt
set FRM_DATA_DIR=demo_data && python main.py
```
A yellow **"DEMO DATA — synthetic records"** badge is shown in the sidebar. Start the app normally
(launcher or `python main.py` in a new terminal) to return to your real data.

---

## 11. Updating, moving or uninstalling

* **Moving the folder:** delete the hidden `.venv` folder inside it after moving, then run the
  launcher again (it rebuilds in 1–3 minutes). Your records are not affected.
  (Show hidden files: Windows Explorer → View → Show → Hidden items; Mac Finder → Cmd+Shift+.)
* **Updating to a newer version:** extract the new ZIP to a new folder and use its launcher. Your
  records stay in your user data folder and appear automatically.
* **Removing your data:** in the app, **Settings → Delete stored data**.
* **Uninstalling the app:** delete the `FacialRecoveryMonitor` folder. To also remove your data,
  delete the data folder (Windows `%APPDATA%\FacialRecoveryMonitor`, Mac
  `~/Library/Application Support/FacialRecoveryMonitor`, Linux
  `~/.local/share/FacialRecoveryMonitor`). Python can be removed via Windows *Settings → Apps* or
  on a Mac by deleting `/Applications/Python 3.12`.

---

## 12. Troubleshooting

| Problem | What to do |
|---|---|
| **Windows: "Windows protected your PC"** | Click **More info → Run anyway**. |
| **Mac: "cannot be opened because it is from an unidentified developer"** | Right-click `START_MAC.command` → **Open** → **Open**, or System Settings → Privacy & Security → **Open Anyway**. |
| **Mac: "permission denied" / file opens in a text editor** | Open Terminal and run `chmod +x ~/Documents/FacialRecoveryMonitor/START_MAC.command` (adjust the path), then try again. |
| The black/Terminal window closes immediately or shows an error | Read the message: it explains the problem. To retry the setup from scratch, delete the hidden `.venv` folder and run the launcher again. |
| "Python could not be found or installed" | Run the installer in `installers/` yourself (Windows: tick **Add python.exe to PATH** → **Install Now**), then run the launcher again. |
| "Offline packages do not match this Python version" | You have a different Python version (not 3.12). The launcher then downloads packages instead — connect to the internet, or install Python 3.12 from `installers/`, delete `.venv`, and retry. |
| **Camera unavailable (Mac)** | System Settings → **Privacy & Security → Camera** → turn on **Terminal** (or **Visual Studio Code**), then quit Terminal completely (Cmd+Q) and start again. |
| **Camera unavailable (Windows)** | Settings → **Privacy & security → Camera** → turn on *Camera access* and *Let desktop apps access your camera*. Close Zoom/Teams/other apps using the camera. |
| Wrong camera (e.g. external webcam not used) | In Facial Check-In or Settings press **Scan**, then choose another camera number. |
| "No face detected" | Face a window or lamp, make sure your whole face is in view, remove hat/sunglasses, sit about an arm's length away, and look straight at the camera. |
| "Facial landmark detection is unavailable" | Settings → Application → **Check face detection** shows the reason. Usually the MediaPipe package did not install — delete `.venv` and run the launcher again (use Python 3.12). |
| Text looks tiny or huge | The app follows your system display scaling; change it in your OS display settings. The window can be resized. |
| Linux: `libEGL.so.1` or `libGL.so.1` not found | `sudo apt install libegl1 libgl1 libgles2` |
| Something else went wrong | The app writes details to a log file (path shown in **Settings → Application → Log file**). Start with the environment variable `FRM_DEV=1` to see technical details in error dialogs. |
