#!/usr/bin/env bash
# Facial Recovery Monitor - launcher for Linux (installs packages online on first run).
# Needs Python >= 3.10 with Tkinter, e.g. on Ubuntu/Debian:
#   sudo apt install python3 python3-venv python3-tk libegl1 libgl1
set -e
cd "$(dirname "$0")"
VENV="$(pwd)/.venv"
if [ ! -f "$VENV/installed.txt" ]; then
  PYEXE=""
  for c in python3.12 python3.11 python3.13 python3.10 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      PYEXE="$c"; break
    fi
  done
  if [ -z "$PYEXE" ]; then
    echo "Python >= 3.10 with Tkinter not found. Install it, e.g.:"
    echo "  sudo apt install python3 python3-venv python3-tk libegl1 libgl1"
    exit 1
  fi
  echo "Using $PYEXE"
  [ -x "$VENV/bin/python" ] || "$PYEXE" -m venv "$VENV"
  "$VENV/bin/python" -m pip install --disable-pip-version-check -r requirements.txt
  echo ok > "$VENV/installed.txt"
fi
exec "$VENV/bin/python" main.py
