@echo off
cd /d "%~dp0"
if not exist venv (
    python -m venv venv
    call .\venv\Scripts\pip install websockets
)
call .\venv\Scripts\python web_bridge.py
pause
