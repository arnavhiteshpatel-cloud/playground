#!/bin/bash
# ==========================================================================
#  Facial Recovery Monitor - one-click launcher for macOS
#  First run: finds (or installs) Python 3.12, creates a private environment
#  in ".venv" and installs the app's packages (offline on Apple-silicon Macs).
#  If macOS says it "cannot be opened": right-click this file -> Open -> Open.
# ==========================================================================
cd "$(dirname "$0")" || exit 1
HERE="$(pwd)"
VENV="$HERE/.venv"
echo
echo "  Facial Recovery Monitor  -  Research Prototype (not a medical device)"
echo "  ---------------------------------------------------------------------"
echo

ok_python() {  # usable = Python >= 3.10 with a working Tkinter
  "$1" -c 'import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1
}

find_python() {
  for c in /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 python3.12 \
           /opt/homebrew/bin/python3.12 /usr/local/bin/python3.12 \
           /Library/Frameworks/Python.framework/Versions/3.11/bin/python3 python3.11 \
           /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 python3.13 python3; do
    if command -v "$c" >/dev/null 2>&1 && ok_python "$c"; then
      PYEXE="$(command -v "$c")"; return 0
    fi
  done
  return 1
}

if [ ! -f "$VENV/installed.txt" ] || [ ! -x "$VENV/bin/python" ]; then
  if ! find_python; then
    echo "  Python 3.12 was not found. The official python.org installer will open now."
    echo "  Click Continue / Agree / Install, enter your Mac password if asked,"
    echo "  and come back to this window when it says 'The installation was successful'."
    open "$HERE/installers/python-3.12.10-macos11.pkg"
    read -r -p "  Press Return here once the Python installation has finished... " _
    if ! find_python; then
      echo "  Python still not found. See LAUNCH_GUIDE.html (Troubleshooting)."
      read -r -p "  Press Return to close." _; exit 1
    fi
  fi
  echo "  Using Python: $PYEXE ($("$PYEXE" -c 'import platform; print(platform.python_version())'))"
  if [ ! -x "$VENV/bin/python" ]; then
    echo "  Creating the app environment in .venv ..."
    "$PYEXE" -m venv "$VENV" || { echo "  Could not create .venv - move this folder to Documents and retry."; read -r _; exit 1; }
  fi
  echo "  Installing app components (first run only, 1-3 minutes)..."
  PYVER="$("$VENV/bin/python" -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"
  INSTALLED=0
  if [ "$(uname -m)" = "arm64" ] && [ "$PYVER" = "3.12" ]; then
    "$VENV/bin/python" -m pip install --disable-pip-version-check --no-index \
      --find-links "$HERE/offline_packages/macos-apple-silicon" -r "$HERE/requirements.txt" && INSTALLED=1
  fi
  if [ "$INSTALLED" = "0" ]; then
    echo "  Downloading components from the internet (Intel Mac or other Python version)..."
    "$VENV/bin/python" -m pip install --disable-pip-version-check -r "$HERE/requirements.txt" && INSTALLED=1
  fi
  if [ "$INSTALLED" = "0" ]; then
    echo "  Installing the app components failed. See LAUNCH_GUIDE.html (Troubleshooting)."
    read -r -p "  Press Return to close." _; exit 1
  fi
  echo ok > "$VENV/installed.txt"
  echo "  Setup complete."
fi

echo "  Starting the app... keep this window open while you use it."
echo "  (The first time you start a check-in, macOS asks for camera access: click OK.)"
"$VENV/bin/python" "$HERE/main.py"
