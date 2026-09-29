@echo off
setlocal
cd /d "%~dp0"

where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo FFmpeg is not installed or is not in PATH.
    echo Install it from https://ffmpeg.org/download.html, then reopen this window.
    pause
    exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or is not in PATH.
    echo Install it from https://www.python.org/downloads/ and enable Add Python to PATH.
    pause
    exit /b 1
)

python enhance_pro.py
pause
