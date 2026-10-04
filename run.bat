@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║     TikTok Video Enhancer 120 FPS - Windows        ║
echo ╚════════════════════════════════════════════════════╝
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Install from: https://www.python.org/downloads/
    echo Make sure to enable 'Add Python to PATH'
    pause
    exit /b 1
)

echo ✅ Python found
echo Installing dependencies...
pip install opencv-python numpy -q

echo.
echo Starting TikTok Video Enhancer...
echo.

python tiktok_enhancer.py
pause
