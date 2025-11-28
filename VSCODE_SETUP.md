# Visual Studio Code Setup Guide

Hướng dẫn chi tiết setup project Audio Processor trong VS Code từ đầu đến cuối.

---

## 📥 Bước 1: Cài đặt Visual Studio Code

### Windows
1. Truy cập [code.visualstudio.com](https://code.visualstudio.com/)
2. Download **Windows x64 User Installer**
3. Chạy file `.exe` và làm theo hướng dẫn
4. ✅ **Quan trọng:** Check các options sau khi cài:
   - ☑ Add "Open with Code" to context menu
   - ☑ Add to PATH

### macOS
```bash
# Option 1: Download từ website
# Truy cập code.visualstudio.com và download .dmg

# Option 2: Dùng Homebrew (recommended)
brew install --cask visual-studio-code
```

### Linux (Ubuntu/Debian)
```bash
# Cài qua snap (recommended)
sudo snap install --classic code

# Hoặc dùng apt
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

### Kiểm tra cài đặt
```bash
code --version
```

---

## 📂 Bước 2: Mở Project trong VS Code

### Cách 1: Từ Command Line (Khuyến nghị)
```bash
# Di chuyển vào thư mục project
cd audio_processor

# Mở VS Code tại thư mục hiện tại
code .
```

### Cách 2: Từ VS Code Interface
1. Mở VS Code
2. **File** → **Open Folder...** (hoặc `Ctrl+K Ctrl+O`)
3. Chọn thư mục `audio_processor`
4. Click **Select Folder**

### Giao diện VS Code sau khi mở:

```
┌─────────────────────────────────────────────────────────────┐
│ File  Edit  Selection  View  Go  Run  Terminal  Help       │
├───────────┬─────────────────────────────────────────────────┤
│           │                                                  │
│ EXPLORER  │  Welcome Tab                                    │
│           │                                                  │
│ 📁 audio_ │  Get Started                                    │
│   processor│  - Open Folder                                 │
│   │       │  - Clone Repository                             │
│   ├─📄 config.py                                           │
│   ├─📄 transcriber.py                                      │
│   ├─📄 segmenter.py                                        │
│   ├─📄 processor.py                                        │
│   ├─📄 main.py                                             │
│   ├─📄 worker.py                                           │
│   ├─📄 example.py                                          │
│   ├─📄 requirements.txt                                    │
│   ├─📄 setup.sh                                            │
│   ├─📄 README.md                                           │
│   └─ ...                                                    │
│           │                                                  │
└───────────┴─────────────────────────────────────────────────┘
```

---

## 🔌 Bước 3: Cài đặt Extensions (Rất quan trọng!)

### 3.1. Mở Extensions Panel
- Click icon Extensions ở sidebar trái (hoặc `Ctrl+Shift+X`)
- Hoặc: **View** → **Extensions**

### 3.2. Cài các Extensions cần thiết:

#### ⭐ **Python** (Microsoft) - BẮT BUỘC
```
Tìm: "Python"
Publisher: Microsoft
Features: IntelliSense, Linting, Debugging, Code formatting
```

**Cách cài:**
1. Gõ "Python" vào search box
2. Tìm extension từ Microsoft (có logo Microsoft)
3. Click **Install**

#### ⭐ **Pylance** (Microsoft) - KHUYẾN NGHỊ
```
Tìm: "Pylance"
Publisher: Microsoft
Features: Fast Python language server, better IntelliSense
```

#### 🔧 **Python Indent** - HỮU ÍCH
```
Tìm: "Python Indent"
Publisher: Kevin Rose
Features: Auto-correct Python indentation
```

#### 📝 **autoDocstring** - HỮU ÍCH
```
Tìm: "autoDocstring"
Publisher: Nils Werner
Features: Generate Python docstrings automatically
```

#### 🎨 **Better Comments** - TÙY CHỌN
```
Tìm: "Better Comments"
Publisher: Aaron Bond
Features: Colorize comments
```

#### 📊 **GitLens** - TÙY CHỌN
```
Tìm: "GitLens"
Publisher: GitKraken
Features: Git history, blame, etc.
```

### 3.3. Restart VS Code
Sau khi cài extensions, restart VS Code để kích hoạt.

---

## 🐍 Bước 4: Setup Python Interpreter

### 4.1. Mở Command Palette
- **Windows/Linux:** `Ctrl+Shift+P`
- **macOS:** `Cmd+Shift+P`

### 4.2. Select Python Interpreter
1. Gõ: **"Python: Select Interpreter"**
2. Chọn từ danh sách

**Nếu chưa có Python:**
- VS Code sẽ nhắc bạn cài Python
- Download từ [python.org](https://www.python.org/downloads/)

### 4.3. Kiểm tra Python version
Mở Terminal trong VS Code:
- **Terminal** → **New Terminal** (hoặc `` Ctrl+` ``)

```bash
# Kiểm tra Python
python --version
# hoặc
python3 --version

# Kiểm tra pip
pip --version
```

---

## 📦 Bước 5: Tạo Virtual Environment

### 5.1. Mở Terminal trong VS Code

**Quan trọng:** Đảm bảo terminal đang ở thư mục project root (`audio_processor`)

### 5.2. Tạo Virtual Environment

#### Windows:
```powershell
# PowerShell
python -m venv venv

# Nếu gặp lỗi execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Linux/Mac:
```bash
python3 -m venv venv
```

### 5.3. VS Code sẽ tự động phát hiện venv

Sau khi tạo xong, VS Code sẽ hiện popup:

```
┌─────────────────────────────────────────────────┐
│ We noticed a new environment has been created.  │
│ Do you want to select it for the workspace?    │
│                                                  │
│           [ Yes ]        [ No ]                 │
└─────────────────────────────────────────────────┘
```

**Click "Yes"** để chọn venv làm interpreter mặc định.

### 5.4. Kích hoạt Virtual Environment manually (nếu cần)

#### Windows:
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat
```

#### Linux/Mac:
```bash
source venv/bin/activate
```

**Sau khi activate thành công, terminal sẽ hiện:**
```
(venv) PS C:\path\to\audio_processor>
```

---

## 📚 Bước 6: Cài đặt Dependencies

### 6.1. Đảm bảo venv đã được activate
Terminal phải hiện `(venv)` ở đầu dòng.

### 6.2. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 6.3. Cài PyTorch

#### Cho CPU (không có GPU):
```bash
pip install torch==2.1.0 torchaudio==2.1.0
```

#### Cho GPU (NVIDIA CUDA 11.8):
```bash
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
```

### 6.4. Cài các dependencies khác
```bash
pip install -r requirements.txt
```

**Process này sẽ mất vài phút.** VS Code sẽ hiển thị progress trong terminal.

### 6.5. Download NLTK data
```bash
python -c "import nltk; nltk.download('punkt')"
```

### 6.6. Verify installation
```bash
python -c "import whisper, stable_whisper, pydub, nltk, librosa; print('✓ All packages installed successfully!')"
```

---

## ⚙️ Bước 7: Configure VS Code Settings

### 7.1. Tạo `.vscode` folder
VS Code sẽ tự tạo khi bạn thay đổi settings, hoặc tạo manual:

```bash
mkdir .vscode
```

### 7.2. Tạo `settings.json`

**File:** `.vscode/settings.json`

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--line-length=88"
    ],
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true
    },
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```

### 7.3. Tạo `launch.json` (cho debugging)

**File:** `.vscode/launch.json`

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Main Script",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "args": [
                "--input",
                "sample.wav",
                "--output",
                "./output"
            ]
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Example",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/example.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Worker",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/worker.py",
            "console": "integratedTerminal",
            "args": [
                "--id",
                "worker_test",
                "--input",
                "./input",
                "--output",
                "./output"
            ]
        }
    ]
}
```

### 7.4. Tạo `tasks.json` (cho common tasks)

**File:** `.vscode/tasks.json`

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Main Script",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": [
                "main.py",
                "--help"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": [
                "-m",
                "pytest"
            ]
        },
        {
            "label": "Install Dependencies",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/pip",
            "args": [
                "install",
                "-r",
                "requirements.txt"
            ]
        }
    ]
}
```

---

## 🚀 Bước 8: Chạy và Test Code

### 8.1. Test với example.py

1. Mở file `example.py` trong VS Code
2. Click **Run** button (▶️) ở góc trên phải
3. Hoặc press `F5` để debug

### 8.2. Chạy main.py

**Cách 1: Từ Terminal**
```bash
python main.py --help
```

**Cách 2: Dùng Debug Configuration**
1. Press `F5`
2. Chọn "Python: Main Script"
3. Code sẽ chạy với breakpoints (nếu có)

### 8.3. Tạo sample audio để test

Nếu chưa có audio file, download hoặc tạo:

```bash
# Tạo thư mục input
mkdir input

# Download sample audio (nếu có link)
# wget https://example.com/sample.wav -O input/sample.wav

# Hoặc copy audio file của bạn vào
# cp /path/to/your/audio.wav input/
```

### 8.4. Test xử lý audio

```bash
# Process single file
python main.py --input input/sample.wav --output ./output

# View stats
python main.py --stats ./output/sample
```

---

## 🐛 Bước 9: Debug trong VS Code

### 9.1. Set Breakpoints
- Click vào bên trái số dòng → xuất hiện chấm đỏ
- Hoặc press `F9` khi cursor ở dòng cần debug

### 9.2. Start Debugging
- Press `F5`
- Chọn configuration (ví dụ: "Python: Main Script")

### 9.3. Debug Controls

```
┌────────────────────────────────────┐
│ Continue (F5)  │  Step Over (F10)  │
│ Step Into (F11) │ Step Out (Shift+F11)│
│ Restart (Ctrl+Shift+F5) │ Stop (Shift+F5)│
└────────────────────────────────────┘
```

### 9.4. Debug Panel
```
VARIABLES
├─ Local
│  ├─ audio_path: "sample.wav"
│  ├─ config: AppConfig(...)
│  └─ segments: List[TranscriptSegment]
├─ Global
└─ ...

WATCH
(Add expressions to watch)

CALL STACK
├─ process_single_file (processor.py:145)
├─ transcribe_to_sentences (transcriber.py:98)
└─ ...
```

### 9.5. Debug Console
Evaluate expressions while debugging:
```python
>>> len(segments)
45
>>> segments[0].text
'This is the first sentence.'
>>> config.whisper.model_size
'base'
```

---

## 💡 Bước 10: Tips & Tricks trong VS Code

### 10.1. Keyboard Shortcuts quan trọng

| Action | Windows/Linux | macOS |
|--------|--------------|-------|
| Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Quick Open File | `Ctrl+P` | `Cmd+P` |
| Toggle Terminal | `` Ctrl+` `` | `` Cmd+` `` |
| Find in Files | `Ctrl+Shift+F` | `Cmd+Shift+F` |
| Go to Definition | `F12` | `F12` |
| Peek Definition | `Alt+F12` | `Option+F12` |
| Format Document | `Shift+Alt+F` | `Shift+Option+F` |
| Comment/Uncomment | `Ctrl+/` | `Cmd+/` |
| Multi-cursor | `Alt+Click` | `Option+Click` |
| Run File | `Ctrl+F5` | `Ctrl+F5` |
| Debug | `F5` | `F5` |

### 10.2. IntelliSense (Auto-complete)

Khi gõ code, VS Code sẽ suggest:
```python
from processor import Audio   # <- suggests: AudioProcessor
config = AppConfig(
    whisper=Whi               # <- suggests: WhisperConfig
```

Press `Ctrl+Space` để manually trigger IntelliSense.

### 10.3. Quick Documentation

- Hover chuột qua function/class để xem docstring
- Press `Ctrl+K Ctrl+I` để show hover info

### 10.4. Navigate Code

**Go to Definition:**
- Click vào function/class + `F12`
- Hoặc `Ctrl+Click`

**Go to Symbol:**
- `Ctrl+Shift+O` → list all symbols (functions, classes) trong file
- `Ctrl+T` → search symbols trong toàn project

### 10.5. Refactoring

**Rename Symbol:**
- Click vào variable/function → `F2`
- Rename sẽ update tất cả references

**Extract Method:**
- Select code → `Ctrl+Shift+R` → "Extract Method"

### 10.6. Code Formatting

**Format Document:**
- `Shift+Alt+F` (Windows/Linux)
- `Shift+Option+F` (macOS)

**Format on Save:**
- Đã enable trong settings.json

### 10.7. Git Integration

VS Code có built-in Git support:

**Source Control Panel (Ctrl+Shift+G):**
```
SOURCE CONTROL
├─ Changes (5)
│  ├─ M config.py
│  ├─ M main.py
│  ├─ A new_feature.py
│  └─ ...
└─ Staged Changes (0)

Message: "Add new feature"
[✓] Commit  [↑] Push
```

**Common Git commands:**
- `Ctrl+Shift+G` → Open Source Control
- Click `+` next to file → Stage
- Enter message → `Ctrl+Enter` → Commit

### 10.8. Integrated Terminal Tips

**Multiple terminals:**
- Click `+` để tạo terminal mới
- `Ctrl+Shift+5` → Split terminal

**Switch between terminals:**
- Dropdown menu ở terminal panel

**Clear terminal:**
- `Ctrl+K` (hoặc gõ `clear`)

### 10.9. Workspace Recommendations

Tạo file `.vscode/extensions.json` để recommend extensions:

```json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "njpwerner.autodocstring",
        "aaron-bond.better-comments"
    ]
}
```

Khi team members mở project, VS Code sẽ suggest cài extensions này.

---

## 📁 Bước 11: File Organization trong VS Code

### 11.1. Explorer View Structure

```
EXPLORER
├─📁 audio_processor
│  ├─📁 .vscode/
│  │  ├─ settings.json
│  │  ├─ launch.json
│  │  └─ tasks.json
│  ├─📁 venv/              (Hidden in Explorer)
│  ├─📁 input/
│  ├─📁 output/
│  ├─📁 temp/
│  ├─📄 config.py
│  ├─📄 transcriber.py
│  ├─📄 segmenter.py
│  ├─📄 processor.py
│  ├─📄 main.py
│  ├─📄 worker.py
│  ├─📄 example.py
│  ├─📄 requirements.txt
│  ├─📄 setup.sh
│  ├─📄 setup.bat
│  ├─📄 .gitignore
│  └─📄 README.md
```

### 11.2. Hide unwanted files/folders

Already configured in `.vscode/settings.json`:
```json
"files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true
}
```

---

## 🔍 Bước 12: Search & Replace

### 12.1. Search in Files
- `Ctrl+Shift+F` → Open Search panel
- Enter search term
- Use regex: click `.*` button
- Case sensitive: click `Aa` button

### 12.2. Replace in Files
- `Ctrl+Shift+H`
- Enter search term and replacement
- Preview changes before replace
- Click "Replace All"

**Example:**
```
Search: model_size="base"
Replace: model_size="small"
```

---

## 🧪 Bước 13: Testing trong VS Code

### 13.1. Cài pytest (nếu có tests)
```bash
pip install pytest
```

### 13.2. Run tests
```bash
# Từ terminal
pytest

# Hoặc dùng Task
Ctrl+Shift+P → "Tasks: Run Task" → "Run Tests"
```

### 13.3. Test Explorer (nếu có tests)
- Install extension: **Python Test Explorer**
- Tests sẽ hiện trong sidebar

---

## 📝 Bước 14: Snippets & Templates

### 14.1. Built-in Python Snippets

Gõ shortcut và press `Tab`:

- `class` → class template
- `def` → function template
- `for` → for loop
- `if` → if statement
- `try` → try-except block

### 14.2. Custom Snippets

**File** → **Preferences** → **User Snippets** → **python.json**

Example custom snippet:
```json
{
    "Audio Processor Function": {
        "prefix": "apfunc",
        "body": [
            "def ${1:function_name}(self, ${2:args}):",
            "    \"\"\"",
            "    ${3:Description}",
            "    ",
            "    Args:",
            "        ${2:args}: ${4:description}",
            "    ",
            "    Returns:",
            "        ${5:return_type}: ${6:description}",
            "    \"\"\"",
            "    ${0:pass}"
        ],
        "description": "Audio Processor function template"
    }
}
```

Sử dụng: Gõ `apfunc` + `Tab`

---

## 🎨 Bước 15: Themes & Appearance (Optional)

### 15.1. Change Color Theme
- `Ctrl+K Ctrl+T` → Select theme
- Popular: Dark+ (default), One Dark Pro, Dracula

### 15.2. File Icons
- Install: **Material Icon Theme**
- `Ctrl+Shift+P` → "File Icon Theme" → Select

### 15.3. Font
Settings → "Font Family" → Suggest: **Fira Code, JetBrains Mono**

Enable ligatures:
```json
"editor.fontFamily": "Fira Code",
"editor.fontLigatures": true
```

---

## ✅ Checklist: Hoàn thành Setup

- [ ] VS Code installed
- [ ] Project opened in VS Code
- [ ] Python extension installed
- [ ] Python interpreter selected
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`requirements.txt`)
- [ ] NLTK data downloaded
- [ ] `.vscode` folder configured
- [ ] Can run `main.py --help` successfully
- [ ] Debug configuration working
- [ ] Tested with sample audio file

---

## 🆘 Troubleshooting trong VS Code

### ❌ "Python not found"
**Solution:**
1. Open Command Palette (`Ctrl+Shift+P`)
2. "Python: Select Interpreter"
3. Choose correct Python version
4. Restart VS Code

### ❌ Import errors (red squiggles)
**Solution:**
1. Ensure venv is activated
2. Check Python interpreter: Bottom-left corner
3. Reinstall packages: `pip install -r requirements.txt`
4. Reload Window: `Ctrl+Shift+P` → "Developer: Reload Window"

### ❌ IntelliSense không hoạt động
**Solution:**
1. Check Pylance extension installed
2. Settings → "Python: Language Server" → "Pylance"
3. Reload Window

### ❌ Terminal không activate venv automatically
**Solution:**
Add to `.vscode/settings.json`:
```json
"python.terminal.activateEnvironment": true
```

### ❌ Formatter không hoạt động
**Solution:**
```bash
pip install black
```
Settings → "Format On Save" → Enable

---

## 🎓 Tài nguyên học thêm

- **VS Code Python Tutorial:** https://code.visualstudio.com/docs/python/python-tutorial
- **VS Code Shortcuts:** https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf
- **Python in VS Code:** https://code.visualstudio.com/docs/languages/python

---

**🎉 Chúc mừng! Bạn đã setup xong Audio Processor project trong VS Code!**

Bây giờ bạn có thể:
- ✅ Edit code với IntelliSense
- ✅ Debug với breakpoints
- ✅ Run tests
- ✅ Git integration
- ✅ Professional development environment

**Next steps:** Bắt đầu code và customize project theo nhu cầu của bạn!
