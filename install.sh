#!/bin/bash

# Audio Processor Installation Script
# For Linux and macOS

set -e

echo "=========================================="
echo "Audio Text Segmentation Tool - Installer"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo -e "${GREEN}✓ Python version: $(python3 --version)${NC}"
    
    # Check if version is >= 3.9
    if [ $(echo "$PYTHON_VERSION >= 3.9" | bc) -eq 0 ]; then
        echo -e "${RED}✗ Python 3.9 or higher is required${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓ FFmpeg is installed${NC}"
    ffmpeg -version | head -n 1
else
    echo -e "${YELLOW}⚠ FFmpeg not found${NC}"
    echo "Installing FFmpeg..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y ffmpeg
        elif command -v yum &> /dev/null; then
            sudo yum install -y ffmpeg
        else
            echo -e "${RED}Please install FFmpeg manually${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo -e "${RED}Please install Homebrew first: https://brew.sh${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✓ FFmpeg installed${NC}"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}venv already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing Python dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Installation Complete!"
echo "==========================================${NC}"
echo ""
echo "To get started:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python main.py           (GUI)"
echo "     python cli.py --help     (CLI)"
echo ""
echo "  3. See Quick Start Guide:"
echo "     cat QUICKSTART.md"
echo ""
echo "Happy processing! 🎉"
