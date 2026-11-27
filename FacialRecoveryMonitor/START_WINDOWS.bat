@echo off
REM ==========================================================================
REM  Facial Recovery Monitor - one-click launcher for Windows
REM  First run: finds (or installs) Python 3.12, creates a private environment
REM  in the ".venv" folder and installs the app's packages from the bundled
REM  "offline_packages" folder (no internet needed). Later runs start at once.
REM ==========================================================================
setlocal EnableExtensions
title Facial Recovery Monitor
cd /d "%~dp0"
set "HERE=%~dp0"
set "VENV=%HERE%.venv"
set "VPY=%VENV%\Scripts\python.exe"
set "VPYW=%VENV%\Scripts\pythonw.exe"
set "USERPY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

echo.
echo   Facial Recovery Monitor  -  Research Prototype (not a medical device)
echo   ---------------------------------------------------------------------
echo.

if not exist "%VENV%\installed.txt" goto setup
if not exist "%VPYW%" goto setup
goto launch

:setup
REM ---------- 1. Find a suitable Python (3.10+ with Tkinter) ---------------
set "PYEXE="
call :try_launcher -3.12
if not defined PYEXE call :try_exe "%USERPY%"
if not defined PYEXE call :try_launcher -3.11
if not defined PYEXE call :try_launcher -3.13
if not defined PYEXE call :try_launcher -3.10
if not defined PYEXE call :try_path
if defined PYEXE goto have_python

echo   Python 3.12 was not found on this computer.
echo   The bundled official installer from python.org can install it for your
echo   user account only (no administrator rights needed).
echo.
choice /C YN /M "  Install Python 3.12 now"
if errorlevel 2 goto no_python
echo.
echo   Installing Python 3.12 - please wait, this takes about a minute...
start "" /wait "%HERE%installers\python-3.12.10-amd64.exe" /passive InstallAllUsers=0 InstallLauncherAllUsers=0 PrependPath=1 Include_launcher=1 Include_tcltk=1 Include_test=0
call :try_exe "%USERPY%"
if not defined PYEXE goto no_python

:have_python
echo   Using Python: %PYEXE%

REM ---------- 2. Create the private environment ----------------------------
if exist "%VPY%" goto install
echo   Creating the app environment in .venv ...
%PYEXE% -m venv "%VENV%"
if errorlevel 1 goto venv_failed

:install
REM ---------- 3. Install packages (offline first, then online) -------------
echo   Installing app components (first run only, 1-3 minutes)...
"%VPY%" -m pip install --disable-pip-version-check --no-index --find-links "%HERE%offline_packages\windows-x64" -r "%HERE%requirements.txt"
if not errorlevel 1 goto installed
echo.
echo   Offline packages do not match this Python version - downloading instead...
"%VPY%" -m pip install --disable-pip-version-check -r "%HERE%requirements.txt"
if errorlevel 1 goto install_failed

:installed
echo ok> "%VENV%\installed.txt"
echo   Setup complete.

:launch
echo   Starting the app... (this window will close)
start "" "%VPYW%" "%HERE%main.py"
exit /b 0

REM ======================= helper subroutines ==============================
:try_launcher
py %1 -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set "PYEXE=py %1"
exit /b 0

:try_exe
if not exist "%~1" exit /b 0
"%~1" -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set PYEXE="%~1"
exit /b 0

:try_path
python -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if not errorlevel 1 set "PYEXE=python"
exit /b 0

:no_python
echo.
echo   Python could not be found or installed automatically.
echo   Double-click installers\python-3.12.10-amd64.exe, tick
echo   "Add python.exe to PATH", click "Install Now", then run this file again.
echo   See LAUNCH_GUIDE.html for help.
pause
exit /b 1

:venv_failed
echo.
echo   Could not create the app environment in "%VENV%".
echo   Move this folder somewhere you can write to (for example Documents)
echo   and try again. See LAUNCH_GUIDE.html - Troubleshooting.
pause
exit /b 1

:install_failed
echo.
echo   Installing the app components failed. Check your internet connection or
echo   install Python 3.12 from the "installers" folder, delete the ".venv"
echo   folder and run this file again. See LAUNCH_GUIDE.html - Troubleshooting.
pause
exit /b 1
