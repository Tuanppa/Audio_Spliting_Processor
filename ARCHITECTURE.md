# Architecture Documentation

Giải thích chi tiết kiến trúc và cách hoạt động của Audio Processor.

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INPUT                          │
│                    (Audio Files + Config)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      ENTRY POINTS                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   main.py    │  │  worker.py   │  │  example.py  │     │
│  │  (CLI Mode)  │  │ (Multi-node) │  │ (Python API) │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSOR LAYER                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              AudioProcessor (processor.py)          │   │
│  │  • Orchestrates entire workflow                     │   │
│  │  • Manages single/batch processing                  │   │
│  │  • Handles errors and logging                       │   │
│  └──────────┬────────────────────────────┬──────────────┘   │
└─────────────┼────────────────────────────┼──────────────────┘
              │                            │
    ┌─────────▼─────────┐        ┌────────▼─────────┐
    │   TRANSCRIBER     │        │    SEGMENTER     │
    │ (transcriber.py)  │        │  (segmenter.py)  │
    └─────────┬─────────┘        └────────┬─────────┘
              │                            │
              ▼                            ▼
    ┌─────────────────────┐    ┌──────────────────────┐
    │  Whisper + Stable-TS │    │   PyDub + SoundFile │
    │  (Speech Recognition)│    │  (Audio Processing) │
    └─────────────────────┘    └──────────────────────┘
              │                            │
              └────────────┬───────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                           │
│  • Individual audio/text files (segment_0001.wav/txt)      │
│  • Full transcript (text + JSON)                           │
│  • Manifest (metadata JSON)                                │
│  • Statistics (metadata.json)                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Core Components

### 1. **config.py** - Configuration Management

**Purpose:** Quản lý tất cả cấu hình của hệ thống

**Key Classes:**
- `WhisperConfig`: Cấu hình Whisper model (model_size, device, language)
- `AudioConfig`: Cấu hình audio processing (sample_rate, format, segment duration)
- `ProcessConfig`: Cấu hình xử lý (output format, batch size, naming)
- `PathConfig`: Quản lý đường dẫn (input/output/temp directories)
- `AppConfig`: Tổng hợp tất cả configs

**Why Pydantic?**
- Type validation tự động
- Config serialization (JSON)
- Clear error messages

---

### 2. **transcriber.py** - Speech Recognition

**Purpose:** Chuyển audio thành text với timestamp chính xác

**Key Classes:**
- `TranscriptSegment`: Data model cho một đoạn transcript
- `AudioTranscriber`: Main transcription engine

**Workflow:**
```
Audio File → Whisper Model → Raw Segments → Stable-TS Alignment
→ Word-level Timestamps → Sentence Splitting → Merged Segments
```

**Key Features:**
- Sử dụng `stable-whisper` cho timestamp chính xác hơn vanilla Whisper
- VAD (Voice Activity Detection) để filter noise
- Smart sentence merging dựa trên punctuation và duration
- Export ra nhiều format (TXT, JSON)

**Why Stable-Whisper?**
- Vanilla Whisper có timestamp không chính xác (± 0.5s)
- Stable-TS refine timestamps bằng mel-spectrogram alignment
- Quan trọng cho việc cắt audio chính xác

---

### 3. **segmenter.py** - Audio Segmentation

**Purpose:** Cắt audio file theo timestamps

**Key Classes:**
- `AudioSegmenter`: Handles audio loading, cutting, exporting

**Workflow:**
```
Audio File → Load & Normalize → Segment According to Timestamps
→ Add Padding → Export Individual Files → Create Manifest
```

**Key Features:**
- Support nhiều audio formats (WAV, MP3, FLAC, etc.)
- Automatic resampling (16kHz for Whisper compatibility)
- Silence padding để tránh cắt mất âm thanh
- Batch export với progress tracking
- Manifest generation (JSON metadata)

**Why PyDub?**
- High-level API dễ dùng
- Support nhiều formats thông qua ffmpeg
- Fast và memory-efficient cho audio manipulation

---

### 4. **processor.py** - Main Orchestrator

**Purpose:** Điều phối toàn bộ workflow

**Key Classes:**
- `AudioProcessor`: Central coordinator

**Workflow:**
```
Input → Transcribe → Segment Text → Cut Audio → Export → Metadata
```

**Key Methods:**
- `process_single_file()`: Xử lý 1 file
- `process_batch()`: Xử lý nhiều files
- `get_processing_stats()`: Tính thống kê

**Responsibilities:**
1. Initialize sub-components (transcriber, segmenter)
2. Manage directories
3. Error handling và retry logic
4. Progress tracking và logging
5. Metadata generation

---

### 5. **main.py** - CLI Entry Point

**Purpose:** Command-line interface

**Features:**
- Argument parsing với argparse
- Logging setup
- Config building từ CLI args
- Single/batch mode switching
- Statistics viewing

**Usage Patterns:**
```bash
# Single file
python main.py --input audio.wav --output ./out

# Batch
python main.py --batch --input-dir ./audios

# Custom model
python main.py --input audio.wav --model large --device cuda
```

---

### 6. **worker.py** - Distributed Processing

**Purpose:** Multi-machine processing

**Architecture:**
```
         Shared Storage (NFS/Network Drive)
                    │
        ┌───────────┼───────────┐
        │           │           │
    Worker 1    Worker 2    Worker 3
    (CPU)       (GPU)       (CPU)
```

**Key Features:**
- File-based locking mechanism
- `.processing` và `.done` markers
- Race condition handling
- Auto-discovery của pending files
- Worker identification

**Locking Mechanism:**
```
audio.wav              # Original file
audio.wav.processing  # Lock marker (JSON with worker_id)
audio.wav.done        # Completion marker (JSON with metadata)
```

**Why This Approach?**
- Simple, no need for queue server (Redis/RabbitMQ)
- Works với any shared storage
- Easy monitoring (just check markers)
- Fault tolerant (can manually reset by deleting markers)

---

## 📊 Data Flow

### Single File Processing

```
1. INPUT
   └─ audio.wav (mono/stereo, any sample rate, any format)

2. TRANSCRIPTION
   ├─ Load audio
   ├─ Resample to 16kHz mono (if needed)
   ├─ Whisper → segments with rough timestamps
   ├─ Stable-TS → refined word-level timestamps
   └─ Sentence merging → final segments

3. SEGMENTATION
   ├─ Load original audio
   ├─ For each segment:
   │  ├─ Extract [start:end] with padding
   │  └─ Export to segment_XXXX.wav
   └─ Create manifest.json

4. OUTPUT
   ├─ segment_0001.wav + segment_0001.txt
   ├─ segment_0002.wav + segment_0002.txt
   ├─ ...
   ├─ full_transcript.txt
   ├─ full_transcript.json
   ├─ manifest.json
   └─ metadata.json
```

---

## 🎯 Design Decisions

### Why Whisper?

**Pros:**
- State-of-the-art accuracy (English ASR)
- Open source, runs locally
- Multiple model sizes (tiny → large)
- Multilingual support (68 languages)

**Cons:**
- Slow trên CPU (especially large models)
- High memory usage
- Timestamp không perfect (needs stable-ts)

**Alternatives considered:**
- Google Speech-to-Text: Paid, needs internet
- Vosk: Faster but less accurate
- Wav2Vec2: Good but needs fine-tuning

### Why Stable-Whisper?

- Whisper's timestamps can be off by 0.5-1s
- Stable-TS adds mel-spectrogram alignment
- Critical for precise audio cutting
- Minimal overhead (~10% slower)

### Why PyDub for Audio?

**Alternatives:**
- librosa: More scientific, slower for simple ops
- scipy.io.wavfile: Low-level, less formats
- soundfile: Great but PyDub is higher-level

PyDub chosen for:
- Simple API
- Format flexibility (via ffmpeg)
- Good documentation

### Why File-Based Locking for Workers?

**Alternatives:**
- Celery + Redis: Complex setup, overkill
- Task queue systems: Need server infrastructure
- Database locking: Need DB setup

File-based locking chosen for:
- Zero infrastructure needed
- Works with any shared storage
- Easy to debug
- Simple to implement

---

## 🔄 Processing Pipeline Details

### Transcription Pipeline

```python
# 1. Load model (one-time)
model = stable_whisper.load_model("base")

# 2. Transcribe
result = model.transcribe(
    audio_path,
    language="en",
    vad=True,          # Filter silence
    mel_first=True,    # Better alignment
    word_timestamps=True
)

# 3. Process segments
for segment in result.segments:
    # Each segment has:
    # - start, end (timestamps)
    # - text (transcribed text)
    # - words (word-level timestamps)
    
# 4. Merge short segments
# Logic: 
# - If segment < min_duration, merge with next
# - If text doesn't end with punctuation, merge
# - If merged > max_duration, don't merge
```

### Segmentation Pipeline

```python
# 1. Load audio
audio = AudioSegment.from_file(path)

# 2. Normalize
audio = audio.set_frame_rate(16000)  # Resample
audio = audio.set_channels(1)         # Mono

# 3. For each transcript segment
for seg in segments:
    start_ms = seg.start * 1000
    end_ms = seg.end * 1000
    
    # Add padding
    start_ms = max(0, start_ms - padding)
    end_ms = min(len(audio), end_ms + padding)
    
    # Cut audio
    chunk = audio[start_ms:end_ms]
    
    # Export
    chunk.export(f"segment_{seg.id:04d}.wav")
```

---

## 💾 Output Formats

### 1. Individual Files

```
output/
├── segment_0001.wav      # Audio segment 1
├── segment_0001.txt      # "This is the first sentence."
├── segment_0002.wav
├── segment_0002.txt
└── ...
```

**Use Case:** TTS training, ASR dataset creation

### 2. Full Transcript

```
[0.00 - 3.45] This is the first sentence.
[3.45 - 7.89] This is the second sentence.
[7.89 - 12.30] And this is the third one.
```

**Use Case:** Subtitles, reference transcription

### 3. Manifest JSON

```json
{
  "total_segments": 100,
  "total_duration": 450.5,
  "segments": [
    {
      "id": 0,
      "audio_file": "segment_0001.wav",
      "text_file": "segment_0001.txt",
      "text": "This is the first sentence.",
      "start": 0.0,
      "end": 3.45,
      "duration": 3.45
    },
    ...
  ]
}
```

**Use Case:** Training data loader, dataset analysis

---

## 🚀 Performance Considerations

### CPU vs GPU

| Model  | CPU (i7)  | GPU (RTX 3060) | Speedup |
|--------|-----------|----------------|---------|
| tiny   | 0.1x RT   | 0.02x RT       | 5x      |
| base   | 0.3x RT   | 0.05x RT       | 6x      |
| small  | 0.6x RT   | 0.08x RT       | 7.5x    |
| medium | 1.5x RT   | 0.15x RT       | 10x     |
| large  | 3.0x RT   | 0.25x RT       | 12x     |

*RT = Real Time (1x RT = 1 phút audio = 1 phút xử lý)*

### Bottlenecks

1. **Transcription** (70-80% of time)
   - Solution: Use GPU, smaller model
   
2. **Audio I/O** (10-15%)
   - Solution: Use SSD, batch processing
   
3. **Segmentation** (5-10%)
   - Negligible, well-optimized

### Optimization Tips

```python
# 1. Use GPU
config = WhisperConfig(device="cuda")

# 2. Use appropriate model
# base for most use cases
# large only if accuracy critical

# 3. Batch processing
processor.process_batch()  # Better than loop

# 4. Multi-machine
# Scale horizontally with workers
```

---

## 🧪 Testing Strategy

### Unit Tests

- `test_config.py`: Config validation
- `test_transcriber.py`: Transcription accuracy
- `test_segmenter.py`: Audio cutting precision
- `test_processor.py`: End-to-end workflow

### Integration Tests

- Full pipeline with sample audio
- Edge cases (silence, noise, music)
- Format compatibility (MP3, FLAC, etc.)

### Performance Tests

- Benchmark different models
- Memory profiling
- Speed comparisons

---

## 📈 Future Enhancements

### Planned Features

1. **Speaker Diarization**
   - Phân biệt nhiều người nói
   - Useful cho interviews, meetings
   
2. **Quality Filtering**
   - Tự động loại bỏ segments có quality thấp
   - WER (Word Error Rate) estimation

3. **Web UI**
   - Drag-and-drop interface
   - Real-time progress
   - Results visualization

4. **Cloud Storage Integration**
   - S3, Google Cloud Storage
   - Azure Blob Storage

5. **API Server**
   - REST API endpoint
   - Job queue management
   - Authentication

---

## 🛠️ Maintenance

### Adding New Audio Format

1. Ensure ffmpeg supports it
2. Test with PyDub: `AudioSegment.from_file(path, format="xxx")`
3. Add to supported formats list

### Updating Whisper Model

```python
# In transcriber.py
model = stable_whisper.load_model("large-v3")  # Latest version
```

### Customizing Segment Merging Logic

```python
# In transcriber.py → transcribe_to_sentences()
should_merge = (
    current_segment.duration < min_duration or
    not current_segment.text.rstrip().endswith(('.', '!', '?'))
    # Add your custom logic here
) and potential_duration <= max_duration
```

---

**For more details, see the code comments in each module.**
