# Quick Start Guide

Get started with Audio Processor in 5 minutes!

---

## ⚡ Super Quick Start

### Linux/Mac
```bash
# 1. Setup (one-time)
chmod +x setup.sh
./setup.sh

# 2. Activate
source venv/bin/activate

# 3. Process your audio
python main.py --input your_audio.wav --output ./results
```

### Windows
```cmd
REM 1. Setup (one-time)
setup.bat

REM 2. Activate
venv\Scripts\activate

REM 3. Process your audio
python main.py --input your_audio.wav --output ./results
```

---

## 📋 What You Get

After processing `your_audio.wav`, you'll get:

```
results/
├── segment_0001.wav      # First sentence audio
├── segment_0001.txt      # First sentence text
├── segment_0002.wav      # Second sentence audio
├── segment_0002.txt      # Second sentence text
├── segment_0003.wav
├── segment_0003.txt
├── ...
├── full_transcript.txt   # Complete transcript with timestamps
├── full_transcript.json  # JSON version
├── manifest.json         # All segments metadata
└── metadata.json         # Processing info
```

---

## 🎯 Common Use Cases

### 1. Create TTS Training Dataset
```bash
# Short segments (1-5 seconds)
python main.py --input audio.wav --min-duration 1.0 --max-duration 5.0
```

### 2. Transcribe Podcast/Lecture
```bash
# Longer segments (5-30 seconds)
python main.py --input podcast.mp3 --min-duration 5.0 --max-duration 30.0
```

### 3. Process Multiple Files
```bash
# Put all audio files in input/ folder
mkdir input
cp *.wav input/

# Batch process
python main.py --batch --input-dir ./input --output-dir ./results
```

### 4. High Accuracy Mode (with GPU)
```bash
# Use large model
python main.py --input audio.wav --model large --device cuda
```

### 5. Fast Preview Mode
```bash
# Use tiny model (10x faster, less accurate)
python main.py --input audio.wav --model tiny
```

---

## 🔧 Common Options

```bash
# Model selection
--model tiny     # Fastest, least accurate (good for testing)
--model base     # DEFAULT - Good balance
--model small    # More accurate
--model medium   # Very accurate
--model large    # Best accuracy (needs GPU)

# Device
--device cpu     # DEFAULT - Works everywhere
--device cuda    # Use GPU (5-10x faster)

# Segment duration
--min-duration 0.5    # Minimum segment length (seconds)
--max-duration 30.0   # Maximum segment length (seconds)

# Output format
--format wav     # DEFAULT - Best quality, large files
--format mp3     # Smaller files

# Verbose output
-v               # Show detailed progress
```

---

## 📊 Check Results

### View Statistics
```bash
python main.py --stats ./results/your_audio
```

**Output:**
```
============================================================
PROCESSING STATISTICS
============================================================
Total Segments: 45
Total Duration: 180.25s (3.00 minutes)
Average Segment: 4.01s
Shortest Segment: 1.20s
Longest Segment: 12.50s
Total Words: 850
Avg Words/Segment: 18.9
============================================================
```

---

## 🚀 Multiple Machines Setup

Perfect for processing large datasets across multiple computers.

### Step 1: Setup Shared Storage
```bash
# Create shared directory (network drive, NAS, or cloud)
mkdir /shared/audio_processing
mkdir /shared/audio_processing/input
mkdir /shared/audio_processing/output
```

### Step 2: Start Workers

**Machine 1 (CPU):**
```bash
python worker.py --id worker_01 \
    --input /shared/audio_processing/input \
    --output /shared/audio_processing/output \
    --model base
```

**Machine 2 (GPU):**
```bash
python worker.py --id worker_02 \
    --input /shared/audio_processing/input \
    --output /shared/audio_processing/output \
    --model large --device cuda
```

**Machine 3 (CPU):**
```bash
python worker.py --id worker_03 \
    --input /shared/audio_processing/input \
    --output /shared/audio_processing/output \
    --model small
```

### Step 3: Add Audio Files
```bash
# Just copy audio files to shared input directory
cp *.wav /shared/audio_processing/input/

# Workers will automatically detect and process them
```

---

## 🐍 Python API Usage

If you prefer coding:

```python
from processor import AudioProcessor
from config import AppConfig, WhisperConfig

# Create config
config = AppConfig(
    whisper=WhisperConfig(
        model_size="base",
        device="cpu"
    )
)

# Initialize processor
processor = AudioProcessor(config)

# Process single file
result = processor.process_single_file(
    audio_path="your_audio.wav",
    output_dir="./output"
)

print(f"Processed {result['total_segments']} segments")
print(f"Duration: {result['total_duration']:.2f}s")
```

See `example.py` for more examples.

---

## 🎓 Tips for Best Results

### Audio Quality
✅ **Good:**
- Clear speech, minimal background noise
- Sample rate: 16kHz or higher
- Format: WAV (lossless)
- Single speaker or distinct speakers

❌ **Problematic:**
- Heavy background music
- Multiple overlapping speakers
- Very low quality recordings
- Extreme accents

### Model Selection

| Use Case | Recommended Model | Device |
|----------|------------------|--------|
| Quick test/preview | `tiny` or `base` | CPU |
| General purpose | `base` or `small` | CPU |
| High accuracy needed | `medium` or `large` | GPU |
| Production dataset | `large` | GPU |

### Segment Duration

- **Short (0.5-3s)**: Speech synthesis, voice cloning
- **Medium (3-10s)**: General ASR training
- **Long (10-30s)**: Transcription, subtitles

---

## ❓ Troubleshooting

### "No speech detected"
- Audio file might be empty/silent
- Try increasing volume
- Check audio format

### Processing too slow
- Use smaller model: `--model tiny` or `--model base`
- Use GPU: `--device cuda`
- Use multiple machines (worker mode)

### Out of memory
- Use smaller model
- Process shorter audio files
- Use `--device cpu`

### Import errors
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### ffmpeg not found
```bash
# Linux
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows - download from https://ffmpeg.org/download.html
```

---

## 📚 Next Steps

1. ✅ **Completed Quick Start** - You can now process audio!

2. 📖 **Read Full Documentation:**
   - [README.md](README.md) - Complete usage guide
   - [INSTALL.md](INSTALL.md) - Detailed installation
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Technical details

3. 🧪 **Try Examples:**
   ```bash
   python example.py
   ```

4. 🎮 **Experiment:**
   - Try different models
   - Adjust segment durations
   - Process your own audio

5. 🚀 **Scale Up:**
   - Setup distributed processing
   - Integrate into your pipeline
   - Build custom workflows

---

## 🆘 Need Help?

- Check [README.md](README.md) for detailed docs
- See [Troubleshooting](#troubleshooting) section
- Review [example.py](example.py) for code samples
- Create GitHub issue
- Email: support@example.com

---

**Happy Processing! 🎵→📝**

*Generated in seconds. Professional results. Zero hassle.*
