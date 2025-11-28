# Installation Guide - Audio Processor

Hướng dẫn cài đặt chi tiết cho từng hệ điều hành.

---

## 📋 Yêu cầu cơ bản

- **Python**: 3.8 hoặc cao hơn
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB+)
- **Disk**: 5GB+ cho Whisper models
- **Optional**: NVIDIA GPU với CUDA (để xử lý nhanh hơn)

---

## 🐧 Linux (Ubuntu/Debian)

### 1. Cài đặt Python và dependencies hệ thống

```bash
# Update package list
sudo apt update

# Cài Python 3 và pip
sudo apt install python3 python3-pip python3-venv

# Cài ffmpeg (required cho audio processing)
sudo apt install ffmpeg

# Kiểm tra version
python3 --version  # Phải >= 3.8
```

### 2. Clone/Download project

```bash
# Nếu có git
git clone <repository-url>
cd audio_processor

# Hoặc download và giải nén
wget <download-url>
unzip audio_processor.zip
cd audio_processor
```

### 3. Chạy setup script (Recommended)

```bash
# Cấp quyền execute
chmod +x setup.sh

# Chạy script
./setup.sh
```

Script sẽ tự động:
- Tạo virtual environment
- Cài đặt tất cả dependencies
- Download NLTK data
- Test installation

### 4. Manual setup (Alternative)

```bash
# Tạo virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Cài PyTorch (CPU)
pip install torch==2.1.0 torchaudio==2.1.0

# Hoặc PyTorch (CUDA 11.8 nếu có GPU)
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118

# Cài các package khác
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"
```

### 5. Kiểm tra cài đặt

```bash
python main.py --help
```

---

## 🍎 macOS

### 1. Cài Homebrew (nếu chưa có)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Cài Python và ffmpeg

```bash
# Cài Python
brew install python@3.11

# Cài ffmpeg
brew install ffmpeg

# Kiểm tra
python3 --version
```

### 3. Setup project

```bash
# Download project
cd ~/Downloads
# ... unzip hoặc git clone

# Chạy setup
cd audio_processor
chmod +x setup.sh
./setup.sh
```

### 4. Manual setup (Alternative)

```bash
# Tạo venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install torch==2.1.0 torchaudio==2.1.0
pip install -r requirements.txt

# Download NLTK
python -c "import nltk; nltk.download('punkt')"
```

---

## 🪟 Windows

### 1. Cài Python

1. Download Python từ [python.org](https://www.python.org/downloads/)
2. Chạy installer, **quan trọng**: Check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   ```

### 2. Cài ffmpeg

**Option A: Sử dụng Chocolatey (Recommended)**

```powershell
# Cài Chocolatey (nếu chưa có)
# Chạy PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Cài ffmpeg
choco install ffmpeg
```

**Option B: Manual installation**

1. Download ffmpeg từ [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. Giải nén vào `C:\ffmpeg`
3. Thêm `C:\ffmpeg\bin` vào System PATH:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit "Path" → Add `C:\ffmpeg\bin`

### 3. Setup project

**Sử dụng Command Prompt hoặc PowerShell:**

```cmd
# Di chuyển vào thư mục project
cd audio_processor

# Tạo virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Cài PyTorch (CPU)
pip install torch==2.1.0 torchaudio==2.1.0

# Hoặc PyTorch (CUDA 11.8 nếu có NVIDIA GPU)
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118

# Cài các dependencies khác
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"
```

### 4. Kiểm tra

```cmd
python main.py --help
```

---

## 🎮 GPU Support (NVIDIA CUDA)

Để sử dụng GPU acceleration (nhanh hơn 5-10 lần):

### 1. Kiểm tra GPU

```bash
# Linux/Mac
lspci | grep -i nvidia

# Windows
nvidia-smi
```

### 2. Cài CUDA Toolkit

Download và cài [CUDA Toolkit 11.8](https://developer.nvidia.com/cuda-11-8-0-download-archive)

### 3. Cài PyTorch với CUDA

```bash
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
```

### 4. Verify CUDA

```python
import torch
print(torch.cuda.is_available())  # Should return True
print(torch.cuda.get_device_name(0))  # Your GPU name
```

### 5. Sử dụng GPU

```bash
python main.py --input sample.wav --device cuda --model large
```

---

## 🔧 Troubleshooting

### Python không tìm thấy

**Windows:**
- Cài lại Python, nhớ check "Add to PATH"
- Hoặc dùng đường dẫn đầy đủ: `C:\Python311\python.exe`

**Linux/Mac:**
- Dùng `python3` thay vì `python`
- Hoặc: `sudo apt install python-is-python3` (Ubuntu)

### pip không hoạt động

```bash
# Thử
python -m pip install --upgrade pip

# Hoặc
python3 -m pip install --upgrade pip
```

### ffmpeg không tìm thấy

**Kiểm tra:**
```bash
ffmpeg -version
```

**Nếu không có:**
- Linux: `sudo apt install ffmpeg`
- Mac: `brew install ffmpeg`
- Windows: Xem phần cài ffmpeg ở trên

### CUDA out of memory

**Solutions:**
1. Dùng model nhỏ hơn: `--model base` thay vì `--model large`
2. Process file nhỏ hơn
3. Dùng CPU: `--device cpu`

### Module import error

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Permission denied (Linux/Mac)

```bash
# Cấp quyền
chmod +x setup.sh
chmod +x main.py

# Hoặc chạy với python
python main.py --help
```

---

## 📦 Virtual Environment

### Tại sao cần virtual environment?

- Tách biệt dependencies của project
- Tránh conflict với packages khác
- Dễ dàng cleanup

### Activate venv

```bash
# Linux/Mac
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### Deactivate venv

```bash
deactivate
```

### Xóa venv

```bash
# Linux/Mac
rm -rf venv

# Windows
rmdir /s venv
```

---

## 🚀 Quick Start After Installation

```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Test với sample file
python main.py --input sample.wav --output ./output

# 3. View help
python main.py --help

# 4. Run examples
python example.py
```

---

## 📞 Need Help?

- Check [README.md](README.md) for usage examples
- See [Troubleshooting](#troubleshooting) section
- Create an issue on GitHub
- Email: support@example.com

---

**Installation complete! Ready to process audio! 🎵**
