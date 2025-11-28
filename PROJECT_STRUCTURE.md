# Project Structure

Chi tiết về cấu trúc và chức năng của từng file trong project.

---

## 📁 Directory Tree

```
audio_processor/
├── 📄 Core Python Files
│   ├── config.py           # Configuration management
│   ├── transcriber.py      # Whisper transcription module
│   ├── segmenter.py        # Audio segmentation module
│   ├── processor.py        # Main processing orchestrator
│   ├── main.py            # CLI entry point
│   ├── worker.py          # Distributed processing worker
│   └── example.py         # Usage examples
│
├── 📄 Setup & Installation
│   ├── requirements.txt    # Python dependencies
│   ├── setup.sh           # Linux/Mac setup script
│   ├── setup.bat          # Windows setup script
│   └── .gitignore         # Git ignore rules
│
├── 📚 Documentation
│   ├── README.md          # Main documentation
│   ├── QUICK_START.md     # Quick start guide
│   ├── INSTALL.md         # Installation guide
│   ├── ARCHITECTURE.md    # Technical architecture
│   └── PROJECT_STRUCTURE.md  # This file
│
└── 📂 Runtime Directories (created on first run)
    ├── input/             # Place audio files here
    ├── output/            # Processed results go here
    ├── temp/              # Temporary files
    └── venv/              # Python virtual environment
```

---

## 📄 File Details

### Core Modules

#### `config.py` (4KB)
**Purpose:** Central configuration management

**Contains:**
- `WhisperConfig`: Model settings (size, device, language)
- `AudioConfig`: Audio processing settings
- `ProcessConfig`: Output format and processing options
- `PathConfig`: Directory paths
- `AppConfig`: Combined configuration

**Key Functions:**
- `load_config()`: Load config from JSON
- `save_config()`: Save config to JSON

**Why Important:** Single source of truth for all settings

---

#### `transcriber.py` (8KB)
**Purpose:** Audio-to-text transcription with Whisper

**Contains:**
- `TranscriptSegment`: Data model for transcript chunks
- `AudioTranscriber`: Main transcription engine

**Key Methods:**
- `transcribe()`: Basic transcription with timestamps
- `transcribe_to_sentences()`: Smart sentence-level segmentation
- `save_transcript()`: Export to text file
- `save_transcript_json()`: Export to JSON

**Technologies:**
- OpenAI Whisper (speech recognition)
- Stable-Whisper (improved timestamps)
- NLTK (sentence splitting)

**Processing Flow:**
```
Audio → Whisper → Raw segments → Timestamp refinement 
→ Sentence merging → Final segments
```

---

#### `segmenter.py` (9KB)
**Purpose:** Audio cutting and segmentation

**Contains:**
- `AudioSegmenter`: Audio manipulation engine

**Key Methods:**
- `load_audio()`: Load and normalize audio
- `segment_audio()`: Cut audio by timestamps
- `export_segments()`: Export individual files
- `detect_silence_segments()`: Find silence (optional)
- `export_manifest()`: Create metadata JSON

**Technologies:**
- PyDub (audio manipulation)
- SoundFile (audio I/O)
- librosa (audio analysis)

**Processing Flow:**
```
Audio file → Load → Normalize (16kHz mono) → Cut by timestamps 
→ Add padding → Export segments
```

---

#### `processor.py` (10KB)
**Purpose:** Main workflow orchestrator

**Contains:**
- `AudioProcessor`: Central coordinator

**Key Methods:**
- `process_single_file()`: Process one audio file
- `process_batch()`: Process multiple files
- `get_processing_stats()`: Calculate statistics

**Responsibilities:**
1. Initialize sub-components
2. Manage workflow sequence
3. Error handling
4. Progress tracking
5. Metadata generation

**Complete Workflow:**
```
1. Load config
2. Initialize transcriber and segmenter
3. Transcribe audio → segments with timestamps
4. Cut audio into segments
5. Export files (audio + text)
6. Create manifest and metadata
7. Generate statistics
```

---

#### `main.py` (8KB)
**Purpose:** Command-line interface

**Features:**
- Argument parsing
- Config building from CLI args
- Logging setup
- Single/batch mode handling
- Statistics viewing

**Usage Examples:**
```bash
# Single file
python main.py --input audio.wav --output ./out

# Batch
python main.py --batch --input-dir ./audios

# Custom model
python main.py --input audio.wav --model large --device cuda

# View stats
python main.py --stats ./output/audio
```

---

#### `worker.py` (11KB)
**Purpose:** Distributed multi-machine processing

**Contains:**
- `Worker`: Autonomous processing agent

**Key Features:**
- File-based locking (`.processing` markers)
- Auto-discovery of pending files
- Worker identification
- Completion tracking (`.done` markers)

**Architecture:**
```
        Shared Storage
             │
    ┌────────┼────────┐
    │        │        │
Worker 1  Worker 2  Worker 3
```

**Usage:**
```bash
# Machine 1
python worker.py --id worker_01 --input /shared/in --output /shared/out

# Machine 2
python worker.py --id worker_02 --input /shared/in --output /shared/out --device cuda
```

---

#### `example.py` (7KB)
**Purpose:** Python API usage demonstrations

**Contains:**
- `example_single_file()`: Process one file
- `example_batch_processing()`: Process multiple files
- `example_custom_config()`: Custom settings
- `example_statistics()`: View results
- `example_transcription_only()`: Transcribe without cutting

**For:** Users who want to integrate into Python code

---

### Setup & Installation

#### `requirements.txt` (0.5KB)
**Purpose:** Python package dependencies

**Key Packages:**
- `openai-whisper`: Speech recognition
- `stable-ts`: Improved timestamps
- `pydub`: Audio processing
- `librosa`: Audio analysis
- `nltk`: Natural language processing
- `torch`: Deep learning framework

---

#### `setup.sh` (3KB) - Linux/Mac
**Purpose:** Automated setup script

**What It Does:**
1. ✅ Check Python version (≥3.8)
2. ✅ Create virtual environment
3. ✅ Install PyTorch (CPU/CUDA)
4. ✅ Install all dependencies
5. ✅ Download NLTK data
6. ✅ Create directories
7. ✅ Test installation

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

---

#### `setup.bat` (3KB) - Windows
**Purpose:** Windows setup script

**Same functionality as setup.sh but for Windows**

**Usage:**
```cmd
setup.bat
```

---

#### `.gitignore` (0.3KB)
**Purpose:** Git ignore rules

**Ignores:**
- Python cache (`__pycache__/`)
- Virtual environment (`venv/`)
- Audio files (`*.wav`, `*.mp3`)
- Output directories (`output/`, `temp/`)
- Logs (`*.log`)
- IDE files (`.vscode/`, `.idea/`)
- Processing markers (`*.processing`, `*.done`)

---

### Documentation

#### `README.md` (9KB)
**Purpose:** Main comprehensive documentation

**Sections:**
- Features overview
- System requirements
- Installation guide
- Usage examples
- Configuration options
- Output formats
- Troubleshooting
- Tips & best practices

**For:** First-time users and reference

---

#### `QUICK_START.md` (7KB)
**Purpose:** Get started in 5 minutes

**Sections:**
- Super quick start commands
- Common use cases
- Essential options
- Statistics viewing
- Multi-machine setup
- Troubleshooting

**For:** Users who want to start immediately

---

#### `INSTALL.md` (7KB)
**Purpose:** Detailed installation instructions

**Sections:**
- Linux installation
- macOS installation
- Windows installation
- GPU setup (CUDA)
- Troubleshooting installation issues
- Virtual environment guide

**For:** Users facing installation problems

---

#### `ARCHITECTURE.md` (16KB)
**Purpose:** Technical deep dive

**Sections:**
- System architecture diagram
- Component details
- Data flow
- Design decisions
- Processing pipeline
- Output formats
- Performance considerations
- Future enhancements

**For:** Developers and technical users

---

#### `PROJECT_STRUCTURE.md` (This file)
**Purpose:** Navigate and understand the project

**For:** Understanding what each file does

---

## 🎯 Which Files Do What?

### Want to...

**Start processing audio?**
→ Run `main.py`

**Process on multiple machines?**
→ Run `worker.py` on each machine

**Use in Python code?**
→ Import from `processor.py` (see `example.py`)

**Change settings?**
→ Edit `config.py` or pass CLI args to `main.py`

**Understand how it works?**
→ Read `ARCHITECTURE.md`

**Fix installation issues?**
→ Check `INSTALL.md`

**Get started quickly?**
→ Follow `QUICK_START.md`

**Customize transcription?**
→ Modify `transcriber.py`

**Change audio processing?**
→ Modify `segmenter.py`

**Add new features?**
→ Extend `processor.py`

---

## 🔧 Extension Points

### Add New Audio Format
**File:** `segmenter.py`
**Method:** `load_audio()`
```python
audio = AudioSegment.from_file(path, format="your_format")
```

### Custom Segment Merging
**File:** `transcriber.py`
**Method:** `transcribe_to_sentences()`
```python
# Modify the should_merge logic
should_merge = (
    # Your custom logic here
)
```

### New Output Format
**File:** `segmenter.py`
**Method:** `export_segments()`
```python
# Add new export logic
```

### Custom Whisper Model
**File:** `transcriber.py`
**Class:** `AudioTranscriber.__init__()`
```python
self.model = stable_whisper.load_model("your_model")
```

---

## 📊 File Sizes

| File | Size | Complexity |
|------|------|------------|
| config.py | 4KB | Simple |
| transcriber.py | 8KB | Medium |
| segmenter.py | 9KB | Medium |
| processor.py | 10KB | Medium |
| main.py | 8KB | Simple |
| worker.py | 11KB | Medium |
| example.py | 7KB | Simple |

**Total Code:** ~57KB (very lightweight!)

---

## 🧪 Testing Files

Currently, the project includes example usage but not unit tests. To add:

```
tests/
├── test_config.py
├── test_transcriber.py
├── test_segmenter.py
├── test_processor.py
└── test_integration.py
```

---

## 📦 Dependencies Size

After installation:
- **Python packages:** ~3GB (mostly PyTorch)
- **Whisper models:** 
  - tiny: 75MB
  - base: 150MB
  - small: 500MB
  - medium: 1.5GB
  - large: 3GB
- **NLTK data:** ~10MB

**Total:** 3-7GB depending on model choice

---

## 🚀 Deployment Structure

For production:

```
production/
├── audio_processor/        # Core code
├── config/
│   └── production.json    # Production config
├── logs/
│   └── *.log             # Application logs
├── shared/               # For distributed setup
│   ├── input/
│   └── output/
└── scripts/
    ├── start_worker.sh
    └── monitor.sh
```

---

## 📝 Code Statistics

- **Total Lines:** ~1,500 lines
- **Modules:** 7 core modules
- **Functions:** ~40 functions
- **Classes:** 5 main classes
- **Documentation:** 4 detailed guides

**Code Quality:**
- Fully typed with type hints
- Comprehensive docstrings
- Error handling throughout
- Logging at all levels

---

**For questions about specific files, see their inline comments and docstrings.**
