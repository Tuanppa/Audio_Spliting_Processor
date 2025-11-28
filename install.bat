@echo off
REM Audio Processor Installation Script for Windows

echo ==========================================
echo Audio Text Segmentation Tool - Installer
echo ==========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9 or higher
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check FFmpeg
echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] FFmpeg not found
    echo.
    echo Please install FFmpeg:
    echo   Option 1: choco install ffmpeg
    echo   Option 2: Download from https://ffmpeg.org/download.html
    echo            and add to PATH
    echo.
    set /p continue="Continue without FFmpeg? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
) else (
    echo [OK] FFmpeg is installed
    ffmpeg -version 2>&1 | findstr "ffmpeg version"
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo [INFO] venv already exists, skipping...
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing Python dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

echo.
echo ==========================================
echo [OK] Installation Complete!
echo ==========================================
echo.
echo To get started:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate.bat
echo.
echo   2. Run the application:
echo      python main.py           (GUI)
echo      python cli.py --help     (CLI)
echo.
echo   3. See Quick Start Guide:
echo      type QUICKSTART.md
echo.
echo Happy processing!
echo.
pause
