@echo off
REM Start HYDRA Scanner v3.0 on Windows

echo.
echo ================================
echo HYDRA Scanner v3.0
echo ================================
echo.

REM Check if venv exists
if not exist venv (
    echo ERROR: Virtual environment not found
    echo Please run setup_windows.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and start scanner
call venv\Scripts\activate.bat
cls
echo Activating virtual environment...
echo.
python scanner_v3.py

pause
