@echo off

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate

if not exist .venv\deps_installed.txt (
    pip install -r requirements.txt
    echo done > .venv\deps_installed.txt
)

python cli.py
pause