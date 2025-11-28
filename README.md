# Audio Processor - Audio to Text Segmentation

Ứng dụng Python để chuyển audio thành text và tách thành các đoạn nhỏ theo câu, phục vụ cho việc tạo dataset AI.

## 🎯 Tính năng

- ✅ Chuyển audio thành text với timestamp chính xác (sử dụng Whisper)
- ✅ Tự động tách câu và merge thành segments hợp lý
- ✅ Cắt audio theo từng câu
- ✅ Export ra nhiều định dạng (individual files, manifest JSON)
- ✅ Xử lý batch nhiều file
- ✅ Hỗ trợ triển khai đa máy (distributed processing)
- ✅ Hỗ trợ GPU acceleration
- ✅ Logging và error handling chi tiết

## 📋 Yêu cầu hệ thống

### Cơ bản
- Python 3.8+
- RAM: 4GB+ (8GB+ cho model large)
- Disk: 5GB+ (cho models)

### Khuyến nghị cho xử lý nhanh
- GPU: NVIDIA GPU với CUDA (RTX 3060+)
- RAM: 16GB+
- SSD storage

## 🚀 Cài đặt

### Bước 1: Clone/Download project

```bash
# Nếu có git
git clone <repository-url>
cd audio_processor

# Hoặc download và giải nén
```

### Bước 2: Tạo virtual environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Kích hoạt (Windows)
venv\Scripts\activate
```

### Bước 3: Cài đặt dependencies

#### Cho CPU (không có GPU)
```bash
pip install -r requirements.txt
```

#### Cho GPU (NVIDIA CUDA 11.8)
```bash
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

### Bước 4: Download NLTK data
```bash
python -c "import nltk; nltk.download('punkt')"
```

### Bước 5: Kiểm tra cài đặt
```bash
python main.py --help
```

## 📖 Sử dụng

### 1. Xử lý một file audio

```bash
python main.py --input sample.wav --output ./output
```

**Kết quả:**
```
output/
├── segment_0001.wav
├── segment_0001.txt
├── segment_0002.wav
├── segment_0002.txt
├── ...
├── full_transcript.txt
├── full_transcript.json
├── manifest.json
└── metadata.json
```

### 2. Xử lý batch nhiều file

```bash
# Đặt tất cả audio vào thư mục input/
mkdir input
cp *.wav input/

# Chạy batch processing
python main.py --batch --input-dir ./input --output-dir ./output
```

### 3. Sử dụng model lớn hơn (chính xác hơn)

```bash
# Model base (default) - cân bằng
python main.py --input sample.wav --model base

# Model small - chính xác hơn
python main.py --input sample.wav --model small

# Model medium - rất chính xác (cần RAM nhiều)
python main.py --input sample.wav --model medium

# Model large - chính xác nhất (cần GPU mạnh)
python main.py --input sample.wav --model large --device cuda
```

### 4. Tùy chỉnh độ dài segment

```bash
# Segment ngắn nhất 1s, dài nhất 20s
python main.py --input sample.wav --min-duration 1.0 --max-duration 20.0
```

### 5. Xem thống kê

```bash
python main.py --stats ./output/sample
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

## 🖥️ Triển khai đa máy

Dùng để xử lý lượng lớn audio trên nhiều máy tính.

### Setup

1. **Tạo shared directory** (network drive hoặc NAS)
   ```
   /shared/
   ├── input/     # Đặt audio files vào đây
   └── output/    # Kết quả sẽ được lưu ở đây
   ```

2. **Chạy worker trên mỗi máy**

   ```bash
   # Máy 1 (CPU)
   python worker.py --id worker_01 --input /shared/input --output /shared/output --model base --device cpu
   
   # Máy 2 (GPU)
   python worker.py --id worker_02 --input /shared/input --output /shared/output --model large --device cuda
   
   # Máy 3 (CPU)
   python worker.py --id worker_03 --input /shared/input --output /shared/output --model small --device cpu
   ```

3. **Copy audio files vào shared/input/**
   - Workers sẽ tự động phát hiện và xử lý
   - Không xung đột (mỗi file chỉ được xử lý bởi 1 worker)

### Cơ chế hoạt động

1. Worker scan `shared/input/` để tìm file mới
2. Lock file bằng cách tạo `.processing` marker
3. Xử lý file
4. Lưu kết quả vào `shared/output/`
5. Tạo `.done` marker
6. Lặp lại

### Monitoring

Xem log của worker:
```bash
python worker.py --id worker_01 --input /shared/input --output /shared/output --log-file worker_01.log -v
```

## ⚙️ Cấu hình nâng cao

### Tạo file config tùy chỉnh

```python
from config import AppConfig, WhisperConfig, AudioConfig

# Tạo config
config = AppConfig(
    whisper=WhisperConfig(
        model_size="large",
        device="cuda"
    ),
    audio=AudioConfig(
        min_segment_duration=2.0,
        max_segment_duration=15.0,
        format="mp3"  # Export ra mp3 thay vì wav
    )
)

# Lưu config
from config import save_config
save_config(config, "my_config.json")

# Load và dùng
from config import load_config
config = load_config("my_config.json")
```

### Sử dụng trong Python code

```python
from processor import AudioProcessor
from config import AppConfig

# Khởi tạo
config = AppConfig()
processor = AudioProcessor(config)

# Xử lý file
result = processor.process_single_file("sample.wav", "./output")

# Xử lý batch
results = processor.process_batch("./input", "./output")

# Xem stats
stats = processor.get_processing_stats("./output/sample")
print(stats)
```

## 📊 Format Output

### 1. Individual Files
```
segment_0001.wav      # Audio đoạn 1
segment_0001.txt      # Text đoạn 1
segment_0002.wav      # Audio đoạn 2
segment_0002.txt      # Text đoạn 2
...
```

### 2. Full Transcript (full_transcript.txt)
```
[0.00 - 3.45] This is the first sentence.
[3.45 - 7.89] This is the second sentence.
[7.89 - 12.30] This is the third sentence.
...
```

### 3. Manifest (manifest.json)
```json
{
  "total_segments": 45,
  "total_duration": 180.25,
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

### 4. Metadata (metadata.json)
```json
{
  "status": "success",
  "input_file": "sample.wav",
  "output_dir": "./output/sample",
  "total_segments": 45,
  "total_duration": 180.25,
  "processed_at": "2025-10-27T10:30:45",
  "config": {
    "whisper_model": "base",
    "sample_rate": 16000,
    "format": "wav"
  }
}
```

## 🔧 Troubleshooting

### Lỗi: "No module named 'whisper'"
```bash
pip install openai-whisper
```

### Lỗi: CUDA out of memory
- Dùng model nhỏ hơn: `--model small` hoặc `--model base`
- Hoặc dùng CPU: `--device cpu`

### Lỗi: "ffmpeg not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# MacOS
brew install ffmpeg

# Windows
# Download từ https://ffmpeg.org/download.html
```

### Audio bị cắt không chính xác
- Tăng `--min-duration`: `--min-duration 2.0`
- Thử model lớn hơn: `--model medium`

### Xử lý quá chậm
- Dùng GPU: `--device cuda`
- Dùng model nhỏ hơn: `--model tiny` hoặc `--model base`
- Triển khai đa máy với `worker.py`

## 📝 Supported Audio Formats

- WAV (✅ Recommended)
- MP3
- FLAC
- M4A
- OGG
- AAC

## 🎓 Tips & Best Practices

### 1. Chọn model phù hợp

| Model  | Speed | Accuracy | RAM   | Use Case                    |
|--------|-------|----------|-------|-----------------------------|
| tiny   | ⚡⚡⚡ | ⭐       | 1GB   | Testing, quick preview      |
| base   | ⚡⚡   | ⭐⭐     | 1GB   | **Recommended for most use**|
| small  | ⚡     | ⭐⭐⭐   | 2GB   | Good balance                |
| medium | 🐌    | ⭐⭐⭐⭐ | 5GB   | High accuracy needed        |
| large  | 🐌🐌  | ⭐⭐⭐⭐⭐| 10GB  | Best accuracy, need GPU     |

### 2. Chuẩn bị audio tốt

- Sample rate: 16kHz hoặc cao hơn
- Format: WAV (lossless) tốt nhất
- Audio rõ ràng, ít noise
- Mono channel (nếu có thể)

### 3. Segment duration

- **Ngắn (0.5-3s)**: Tốt cho speech synthesis training
- **Trung bình (3-10s)**: Tốt cho general ASR training
- **Dài (10-30s)**: Tốt cho podcast/lecture transcription

### 4. Distributed processing

- 1 máy GPU mạnh (model large) + nhiều máy CPU (model base)
- Monitor băng thông network nếu dùng network drive
- Dùng SSD cho shared directory nếu có thể

## 📄 License

MIT License - Free to use for any purpose

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create Pull Request

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: your-email@example.com

## 🙏 Acknowledgments

- OpenAI Whisper - Speech recognition model
- Stable-ts - Improved timestamp alignment
- PyDub - Audio processing
- NLTK - Natural language processing

---

**Happy Processing! 🎵→📝**
