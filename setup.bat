@echo off
REM Setup script for Audio Processor on Windows

echo ==========================================
echo Audio Processor - Setup Script (Windows)
echo ==========================================
echo.

REM Check Python version
echo 1. Checking Python version...
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo Python OK
echo.

REM Check if virtual environment exists
echo 2. Setting up virtual environment...
if exist "venv" (
    echo Virtual environment already exists
    set /p recreate="Do you want to recreate it? (y/n): "
    if /i "%recreate%"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo Virtual environment recreated
    )
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo 3. Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo 4. Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1
echo pip upgraded
echo.

REM Install PyTorch
echo 5. Installing PyTorch...
set /p gpu="Do you have NVIDIA GPU with CUDA? (y/n): "
if /i "%gpu%"=="y" (
    echo Installing PyTorch with CUDA 11.8...
    pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
) else (
    echo Installing PyTorch (CPU only)...
    pip install torch==2.1.0 torchaudio==2.1.0
)
echo PyTorch installed
echo.

REM Install other dependencies
echo 6. Installing other dependencies...
pip install -r requirements.txt
echo Dependencies installed
echo.

REM Download NLTK data
echo 7. Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True)"
echo NLTK data downloaded
echo.

REM Create directories
echo 8. Creating directories...
if not exist "input" mkdir input
if not exist "output" mkdir output
if not exist "temp" mkdir temp
echo Directories created
echo.

REM Test installation
echo 9. Testing installation...
python -c "import whisper; import stable_whisper; import pydub; import nltk; import librosa; print('All modules imported successfully!')"
if errorlevel 1 (
    echo ERROR: Some modules failed to import
    echo Please check the error messages above
    pause
    exit /b 1
)
echo All modules working
echo.

echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To activate the environment in the future:
echo   venv\Scripts\activate
echo.
echo To start processing:
echo   python main.py --help
echo.
echo Press any key to exit...
pause > nul
