@echo off
setlocal ENABLEDELAYEDEXPANSION

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not on PATH.
    echo Please install Python 3 and ensure "python" is available in your PATH.
    pause
    exit /b 1
)

where nmap >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Nmap is not installed or not on PATH.
    echo Please install Nmap from https://nmap.org/download.html and ensure "nmap" is available in your PATH.
    pause
    exit /b 1
)

if not exist .venv (
    echo [.venv] Virtual environment not found. Creating one...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment in ".venv".
        pause
        exit /b 1
    )
)

if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate
) else (
    echo [ERROR] Could not find ".venv\Scripts\activate.bat".
    echo The virtual environment seems to be corrupted. Delete ".venv" and re-run this script.
    pause
    exit /b 1
)

if not exist .venv\deps_installed.txt (
    echo Installing Python dependencies from requirements.txt ...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies.
        pause
        exit /b 1
    )
    echo done > .venv\deps_installed.txt
)

python cli.py
if errorlevel 1 (
    echo [ERROR] CLI exited with an error.
)

pause
endlocal