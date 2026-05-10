@echo off
REM Start HYDRA Bot v16.0 on Windows

echo.
echo ================================
echo HYDRA Trading Bot v16.0
echo ================================
echo.

REM Check if venv exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and start bot
call venv\Scripts\activate.bat
cls
echo Activating virtual environment...
echo.
python bot.py

pause
