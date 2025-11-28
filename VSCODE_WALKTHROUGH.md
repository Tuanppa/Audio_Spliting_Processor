# VS Code Walkthrough - Audio Processor Project

Hướng dẫn thực hành từng bước, giống như một video tutorial.

---

## 🎬 Video 1: Setup Project lần đầu (15 phút)

### Scene 1: Cài đặt và mở project (3 phút)

**Bước 1: Mở Terminal/Command Prompt**
```bash
# Trên Windows: Win+R → cmd → Enter
# Trên Mac: Cmd+Space → Terminal → Enter
# Trên Linux: Ctrl+Alt+T
```

**Bước 2: Di chuyển vào thư mục project**
```bash
cd /path/to/audio_processor
# Ví dụ Windows: cd C:\Users\YourName\Documents\audio_processor
# Ví dụ Mac/Linux: cd ~/Documents/audio_processor
```

**Bước 3: Mở VS Code**
```bash
code .
```

**Kết quả:** VS Code mở với thư mục audio_processor

```
VS Code Window Opens
┌─────────────────────────────────────────┐
│ Welcome to Visual Studio Code          │
│                                         │
│ Explorer panel shows:                   │
│ 📁 audio_processor                      │
│   ├─ config.py                         │
│   ├─ transcriber.py                    │
│   ├─ ...                               │
└─────────────────────────────────────────┘
```

---

### Scene 2: Cài Extensions (4 phút)

**Bước 1: Mở Extensions panel**
- Click icon 🧩 ở sidebar trái
- Hoặc press `Ctrl+Shift+X`

**Bước 2: Cài Python extension**
1. Gõ "Python" vào search box
2. Tìm "Python" từ Microsoft (logo Microsoft)
3. Click **Install** button màu xanh
4. Đợi cài đặt (thanh progress ở bottom)

**Bước 3: Cài Pylance extension**
1. Gõ "Pylance"
2. Click **Install**

**Kết quả:** Bottom-right hiện notification
```
┌────────────────────────────────────┐
│ ✓ Extension 'Python' installed    │
│ ✓ Extension 'Pylance' installed   │
└────────────────────────────────────┘
```

**Bước 4: Reload VS Code**
- Press `Ctrl+Shift+P`
- Gõ "Reload Window"
- Press Enter

---

### Scene 3: Setup Python và Virtual Environment (5 phút)

**Bước 1: Mở Terminal trong VS Code**
- Press `` Ctrl+` `` (backtick key)
- Hoặc: **Terminal → New Terminal**

Terminal panel xuất hiện ở bottom:
```
TERMINAL
┌────────────────────────────────────────┐
│ PS C:\...\audio_processor>            │
│ █                                      │
└────────────────────────────────────────┘
```

**Bước 2: Kiểm tra Python**
```bash
python --version
# Expected output: Python 3.8 or higher
```

**Nếu không có Python:**
- Popup sẽ hiện: "Python not found"
- Click "Install Python"
- Hoặc download từ python.org

**Bước 3: Tạo Virtual Environment**

**Windows:**
```powershell
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

**Chờ ~30 giây.** Progress hiển thị:
```
Creating virtual environment...
Installing setuptools...
Installing pip...
Done.
```

**Popup xuất hiện:**
```
┌──────────────────────────────────────────┐
│ We noticed a new environment:            │
│ venv                                     │
│                                          │
│ Select for workspace?                    │
│ [ Yes ]  [ No ]                         │
└──────────────────────────────────────────┘
```

**Bước 4: Click "Yes"**

**Kết quả:** Bottom-left hiển thị:
```
🐍 Python 3.11.x ('venv': venv)
```

**Bước 5: Activate venv trong Terminal**

Terminal sẽ tự động activate, nhưng nếu không:

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Thành công khi terminal hiện:**
```
(venv) PS C:\...\audio_processor>
```

---

### Scene 4: Cài Dependencies (3 phút)

**Bước 1: Upgrade pip**
```bash
python -m pip install --upgrade pip
```

Output:
```
Collecting pip
  Downloading pip-23.x.x...
Successfully installed pip-23.x.x
```

**Bước 2: Cài PyTorch**

**Nếu có GPU NVIDIA:**
```bash
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
```

**Nếu không có GPU (CPU only):**
```bash
pip install torch==2.1.0 torchaudio==2.1.0
```

**Chờ 2-3 phút.** Progress bars sẽ hiện:
```
Downloading torch-2.1.0...
████████████████████ 100%
Installing collected packages...
Successfully installed torch-2.1.0
```

**Bước 3: Cài các packages khác**
```bash
pip install -r requirements.txt
```

**Chờ 2-3 phút.** Nhiều packages sẽ được cài:
```
Collecting openai-whisper
Collecting stable-ts
Collecting pydub
...
Successfully installed 15 packages
```

**Bước 4: Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt')"
```

Output:
```
[nltk_data] Downloading package punkt...
[nltk_data]   Package punkt is already up-to-date!
```

**Bước 5: Verify installation**
```bash
python -c "import whisper, stable_whisper, pydub, nltk, librosa; print('✓ All packages installed!')"
```

**Kết quả thành công:**
```
✓ All packages installed!
```

---

## 🎬 Video 2: Chạy code lần đầu (10 phút)

### Scene 1: Khám phá code (2 phút)

**Bước 1: Mở file config.py**
- Click `config.py` trong Explorer
- Hoặc press `Ctrl+P` → gõ "config" → Enter

**Scroll qua file để xem cấu trúc:**
```python
class WhisperConfig(BaseModel):
    model_size: Literal["tiny", "base", "small", ...
    device: Literal["cuda", "cpu"] = "cpu"
    ...
```

**Bước 2: Hover chuột qua `BaseModel`**
- Tooltip hiện: "from pydantic import BaseModel"
- This shows IntelliSense working

**Bước 3: Press `Ctrl+P` và explore các files:**
- Gõ "trans" → mở transcriber.py
- Gõ "seg" → mở segmenter.py
- Gõ "proc" → mở processor.py
- Gõ "main" → mở main.py

---

### Scene 2: Chuẩn bị test data (2 phút)

**Bước 1: Tạo thư mục input**

Trong terminal:
```bash
mkdir input
```

**Bước 2: Copy audio file vào input/**

**Option A: Có audio file sẵn**
```bash
# Windows
copy C:\path\to\your\audio.wav input\

# Mac/Linux
cp /path/to/your/audio.wav input/
```

**Option B: Download sample audio**
```bash
# Ví dụ: Download từ internet (nếu có link)
# curl -o input/sample.wav https://example.com/sample.wav
```

**Bước 3: Verify file exists**
```bash
ls input/
# hoặc Windows: dir input\
```

Output:
```
input/
└── sample.wav
```

---

### Scene 3: Run code với Terminal (3 phút)

**Bước 1: Xem help**
```bash
python main.py --help
```

Output hiển thị usage:
```
usage: main.py [-h] [--input INPUT] [--output OUTPUT] ...

Audio Processor - Convert audio to text with segmentation

optional arguments:
  --input, -i    Input audio file
  --output, -o   Output directory
  ...
```

**Bước 2: Process audio file**
```bash
python main.py --input input/sample.wav --output ./output
```

**Watching the progress:**
```
2024-10-27 10:30:45 - INFO - Initializing Audio Processor...
2024-10-27 10:30:46 - INFO - Loading Whisper model: base on cpu
2024-10-27 10:30:52 - INFO - Model loaded successfully
============================================================
Processing: sample.wav
Output dir: ./output/sample
============================================================

Step 1/4: Transcribing audio...
████████████████████ 100%
✓ Transcribed 45 segments

Step 2/4: Saving transcript...
✓ Transcript saved

Step 3/4: Segmenting and exporting audio...
Processing segment 0001... ✓
Processing segment 0002... ✓
...
✓ 45 segments exported

Step 4/4: Creating manifest...
✓ Manifest created

============================================================
✓ Processing complete!
  - Segments: 45
  - Duration: 180.25s
  - Output: ./output/sample
============================================================
```

**Bước 3: Xem kết quả**

Trong Explorer, expand output folder:
```
📁 output/
  └─📁 sample/
    ├─ segment_0001.wav
    ├─ segment_0001.txt
    ├─ segment_0002.wav
    ├─ segment_0002.txt
    ├─ ...
    ├─ full_transcript.txt
    ├─ full_transcript.json
    ├─ manifest.json
    └─ metadata.json
```

**Bước 4: Mở một text file để xem**
- Click `segment_0001.txt`
- Xem nội dung transcript

---

### Scene 4: Run với Debug (3 phút)

**Bước 1: Mở file main.py**

**Bước 2: Set breakpoint**
- Click bên trái số dòng 45 (hoặc dòng nào đó)
- Chấm đỏ xuất hiện 🔴

**Bước 3: Start debugging**
- Press `F5`
- Hoặc click icon ▶️ ở top-right → "Start Debugging"

**Popup xuất hiện:**
```
┌────────────────────────────────┐
│ Select a debug configuration   │
│                                │
│ ▶ Python: Main Script         │
│ ▶ Python: Current File        │
│ ▶ Python: Example             │
└────────────────────────────────┘
```

**Bước 4: Chọn "Python: Main Script"**

**Debug starts. Code runs until breakpoint:**
```
┌─────────────────────────────────────┐
│ CALL STACK                          │
├─────────────────────────────────────┤
│ ▶ main (main.py:45)                │
│ ▶ process_single_file (processor.py)│
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ VARIABLES                           │
├─────────────────────────────────────┤
│ Local                               │
│  ├─ args: Namespace(...)           │
│  ├─ config: AppConfig(...)         │
│  └─ processor: AudioProcessor(...) │
└─────────────────────────────────────┘
```

**Bước 5: Step through code**
- Press `F10` (Step Over) để chạy từng dòng
- Xem VARIABLES panel update realtime
- Press `F5` (Continue) để chạy đến breakpoint tiếp theo

**Bước 6: Stop debugging**
- Press `Shift+F5` (Stop)
- Hoặc click 🟥 Stop button

---

## 🎬 Video 3: Customize và Develop (15 phút)

### Scene 1: Change Configuration (3 phút)

**Mục tiêu:** Change model từ "base" sang "small"

**Bước 1: Mở config.py**
```bash
Ctrl+P → "config" → Enter
```

**Bước 2: Find WhisperConfig class**
```bash
Ctrl+F → gõ "WhisperConfig"
```

**Bước 3: Change default model_size**

From:
```python
model_size: Literal["tiny", "base", "small", "medium", "large"] = "base"
```

To:
```python
model_size: Literal["tiny", "base", "small", "medium", "large"] = "small"
```

**Bước 4: Save**
```bash
Ctrl+S
```

Blue dot on tab disappears → file saved.

**Bước 5: Test**
```bash
python main.py --input input/sample.wav --output ./output_small
```

Terminal output shows:
```
Loading Whisper model: small on cpu  # ← Changed!
```

---

### Scene 2: Add a New Feature (5 phút)

**Mục tiêu:** Add function to get word count statistics

**Bước 1: Mở processor.py**

**Bước 2: Scroll to bottom of AudioProcessor class**
```bash
Ctrl+End
```

**Bước 3: Add new method**

Place cursor after last method, press Enter twice, then type:

```python
def get_word_count_stats(self, segments: List[TranscriptSegment]) -> dict:
    """
    Calculate word count statistics
    
    Args:
        segments: List of TranscriptSegment
    
    Returns:
        dict: Statistics about word counts
    """
    word_counts = [len(seg.text.split()) for seg in segments]
    
    return {
        "total_words": sum(word_counts),
        "avg_words_per_segment": sum(word_counts) / len(word_counts) if word_counts else 0,
        "min_words": min(word_counts) if word_counts else 0,
        "max_words": max(word_counts) if word_counts else 0
    }
```

**Bước 4: Format code**
```bash
Shift+Alt+F
```

Code auto-formats với proper indentation.

**Bước 5: Add import if needed**

VS Code may show yellow squiggle under `List`:
- Hover → "Quick Fix"
- Click "Add import from typing"

Auto-adds at top:
```python
from typing import List
```

**Bước 6: Save**
```bash
Ctrl+S
```

**Bước 7: Test new function**

Open example.py and add:
```python
# After processing
stats = processor.get_word_count_stats(segments)
print(stats)
```

Run with `F5` → "Python: Example"

---

### Scene 3: Debug a Problem (4 phút)

**Scenario:** Segments quá ngắn, muốn tìm nguyên nhân

**Bước 1: Mở transcriber.py**

**Bước 2: Find merge logic**
```bash
Ctrl+F → "should_merge"
```

**Bước 3: Set breakpoint**
Click left of line `should_merge = (`

**Bước 4: Start debug**
```bash
F5 → "Python: Example"
```

**Bước 5: When breakpoint hits**

Check VARIABLES:
```
current_segment
  ├─ duration: 0.8  # ← Too short!
  └─ text: "Hello"

min_duration: 0.5
```

**Bước 6: Evaluate in Debug Console**
```python
>>> current_segment.duration
0.8
>>> current_segment.duration < min_duration
False  # ← Not merging because 0.8 > 0.5
```

**Aha moment:** Need to increase `min_duration`!

**Bước 7: Stop debug**
```bash
Shift+F5
```

**Bước 8: Fix**

In main.py or config:
```python
min_duration=2.0  # Increased from 0.5
```

---

### Scene 4: Test with Different Models (3 phút)

**Bước 1: Run with tiny model (fastest)**
```bash
python main.py --input input/sample.wav --model tiny --output ./output_tiny
```

Watch speed (very fast but less accurate).

**Bước 2: Run with small model (balanced)**
```bash
python main.py --input input/sample.wav --model small --output ./output_small
```

Compare accuracy in output files.

**Bước 3: Compare results**

Open both output folders side-by-side:
- `Ctrl+P` → output_tiny/full_transcript.txt
- `Ctrl+\` (split editor)
- `Ctrl+P` → output_small/full_transcript.txt

Visual comparison:
```
Tiny Model                Small Model
─────────────────────────────────────────
"hello world"             "Hello, world!"
"this is test"            "This is a test."
```

Small model has better punctuation!

---

## 🎬 Video 4: Multi-Machine Setup (10 phút)

### Scene 1: Setup Shared Directory (2 phút)

**On Network Drive / NAS:**

```bash
# Create shared folders
mkdir /shared/audio_processing
mkdir /shared/audio_processing/input
mkdir /shared/audio_processing/output
```

**Bước 2: Verify access từ mỗi máy**

**Machine 1:**
```bash
ls /shared/audio_processing/
# Should list: input/ output/
```

**Machine 2:**
```bash
ls /shared/audio_processing/
# Should list: input/ output/
```

---

### Scene 2: Start Workers (3 phút)

**Machine 1: CPU Worker**

Open VS Code terminal:
```bash
python worker.py \
  --id worker_01 \
  --input /shared/audio_processing/input \
  --output /shared/audio_processing/output \
  --model base \
  --device cpu
```

Output:
```
Worker worker_01 initialized
  Input dir: /shared/audio_processing/input
  Output dir: /shared/audio_processing/output
Worker worker_01 starting...
Poll interval: 10s
No pending files, waiting...
```

**Machine 2: GPU Worker**

Open VS Code terminal:
```bash
python worker.py \
  --id worker_02 \
  --input /shared/audio_processing/input \
  --output /shared/audio_processing/output \
  --model large \
  --device cuda
```

Output:
```
Worker worker_02 initialized
  Input dir: /shared/audio_processing/input
  Output dir: /shared/audio_processing/output
Loading Whisper model: large on cuda
Worker worker_02 starting...
```

---

### Scene 3: Add Files to Process (2 phút)

**From any machine, copy audio files:**

```bash
cp ~/audio_files/*.wav /shared/audio_processing/input/
```

**Watch workers pick up files:**

**Machine 1 terminal:**
```
Found 3 pending files
Processing: audio1.wav
Locked file: audio1.wav
Step 1/4: Transcribing...
```

**Machine 2 terminal:**
```
Found 2 pending files
Processing: audio2.wav
Locked file: audio2.wav
Step 1/4: Transcribing...
```

**No conflicts!** Each worker processes different files.

---

### Scene 4: Monitor Progress (3 phút)

**Create monitoring script:** `monitor.sh`

```bash
#!/bin/bash
while true; do
    clear
    echo "=== Audio Processing Monitor ==="
    echo ""
    echo "Pending files:"
    ls /shared/audio_processing/input/*.wav 2>/dev/null | wc -l
    echo ""
    echo "Processing files:"
    ls /shared/audio_processing/input/*.processing 2>/dev/null | wc -l
    echo ""
    echo "Completed files:"
    ls /shared/audio_processing/input/*.done 2>/dev/null | wc -l
    echo ""
    echo "Output folders:"
    ls -1 /shared/audio_processing/output/ | wc -l
    echo ""
    sleep 5
done
```

Run:
```bash
chmod +x monitor.sh
./monitor.sh
```

Output updates every 5 seconds:
```
=== Audio Processing Monitor ===

Pending files: 5
Processing files: 2
Completed files: 10
Output folders: 10

(updates every 5s)
```

---

## 🎬 Video 5: Advanced Tips (10 phút)

### Scene 1: Custom Shortcuts (2 phút)

**Bước 1: Open Keyboard Shortcuts**
```bash
Ctrl+K Ctrl+S
```

**Bước 2: Search "Run Python File"**

**Bước 3: Double-click binding**

**Bước 4: Press desired key (e.g., `F6`)**

Now `F6` runs current Python file!

---

### Scene 2: Code Snippets (2 phút)

**Bước 1: Create custom snippet**

File → Preferences → User Snippets → python.json

**Bước 2: Add:**
```json
{
    "Logger Info": {
        "prefix": "logi",
        "body": [
            "self.logger.info(\"$1\")"
        ]
    }
}
```

**Bước 3: Use it**

In any file, type `logi` → Tab
Auto-expands to:
```python
self.logger.info("|")  # Cursor here
```

---

### Scene 3: Git Integration (3 phút)

**Bước 1: Initialize Git**
```bash
git init
```

**Bước 2: Open Source Control**
```bash
Ctrl+Shift+G
```

**Bước 3: Stage changes**
- Click `+` next to files

**Bước 4: Commit**
- Enter message: "Initial commit"
- `Ctrl+Enter` to commit

**Bước 5: View history**
- Click clock icon
- See commit timeline

---

### Scene 4: Workspace Settings (3 phút)

**Create workspace-specific settings:**

`.vscode/settings.json` (already covered)

**Advanced settings:**
```json
{
    "python.analysis.extraPaths": [
        "./src",
        "./lib"
    ],
    "python.testing.pytestEnabled": true,
    "editor.inlineSuggest.enabled": true,
    "github.copilot.enable": {
        "*": true,
        "python": true
    }
}
```

---

## ✅ Final Checklist

After following all videos:

- [ ] VS Code installed and working
- [ ] Extensions installed (Python, Pylance)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Can run `main.py` without errors
- [ ] Can debug with breakpoints
- [ ] Tested with sample audio file
- [ ] Output files generated correctly
- [ ] Can modify code and see changes
- [ ] Understand basic workflows

---

## 🎓 Next Steps

1. **Practice:** Try processing different audio files
2. **Customize:** Modify code to fit your needs
3. **Experiment:** Try different models and settings
4. **Learn:** Read code comments and documentation
5. **Build:** Add new features you need

---

**🎉 Congratulations! You're now a VS Code + Audio Processor expert!**

**Questions? Tips? → See other documentation files or create an issue on GitHub.**
