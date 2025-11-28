#!/bin/bash
# Setup script for Audio Processor

echo "=========================================="
echo "Audio Processor - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "1. Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python version OK: $python_version"
echo ""

# Create virtual environment
echo "2. Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "3. Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "4. Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install PyTorch (CPU or CUDA)
echo "5. Installing PyTorch..."
read -p "Do you have NVIDIA GPU with CUDA? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing PyTorch with CUDA 11.8..."
    pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
else
    echo "Installing PyTorch (CPU only)..."
    pip install torch==2.1.0 torchaudio==2.1.0
fi
echo "✓ PyTorch installed"
echo ""

# Install other dependencies
echo "6. Installing other dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Download NLTK data
echo "7. Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True)"
echo "✓ NLTK data downloaded"
echo ""

# Create directories
echo "8. Creating directories..."
mkdir -p input output temp
echo "✓ Directories created"
echo ""

# Test installation
echo "9. Testing installation..."
python3 -c "
import whisper
import stable_whisper
import pydub
import nltk
import librosa
print('All modules imported successfully!')
"

if [ $? -eq 0 ]; then
    echo "✓ All modules working"
    echo ""
    echo "=========================================="
    echo "✓ Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "To activate the environment in the future:"
    echo "  source venv/bin/activate"
    echo ""
    echo "To start processing:"
    echo "  python main.py --help"
    echo ""
else
    echo "❌ Some modules failed to import"
    echo "Please check the error messages above"
    exit 1
fi
