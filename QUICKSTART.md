# 🚀 Quick Start Guide

Hướng dẫn bắt đầu nhanh trong 5 phút!

---

## ⚡ Cài đặt nhanh

### 1. Cài đặt Python và FFmpeg

**Python 3.9+** (kiểm tra: `python --version`)

**FFmpeg:**
```bash
# Windows (với Chocolatey)
choco install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Kiểm tra
ffmpeg -version
```

### 2. Clone và cài đặt dependencies

```bash
# Download project
cd audio_processor

# Cài đặt thư viện
pip install -r requirements.txt

# Lần đầu chạy sẽ tự động tải model Whisper
```

---

## 🎯 Cách 1: Sử dụng GUI (Đơn giản nhất)

### Chạy ứng dụng

```bash
python main.py
```

### Sử dụng

1. **Click "Browse"** → Chọn file audio (.wav, .mp3, ...)
2. **Chọn Output Directory** → Nơi lưu kết quả
3. **Chọn Language** → vi (Việt) / en (Anh) / auto (tự động)
4. **Click "▶ Process Audio"** → Đợi xử lý
5. **Click "🗁 Open Output"** → Xem kết quả!

### Kết quả

```
output/
  └── your_audio_file/
      ├── segments/
      │   ├── segment_0001.wav
      │   ├── segment_0001.txt
      │   ├── segment_0002.wav
      │   ├── segment_0002.txt
      │   └── ...
      ├── full_transcript.txt
      ├── manifest.json
      └── metadata.csv
```

---

## 💻 Cách 2: Sử dụng Command Line

### Xử lý 1 file

```bash
python cli.py --audio input.wav --output ./results
```

### Xử lý nhiều files

```bash
python cli.py --batch ./audio_folder --output ./results
```

### Tùy chỉnh

```bash
# Chọn ngôn ngữ
python cli.py --audio input.wav --output ./results --language vi

# Chọn model size (tiny/base/small/medium/large)
python cli.py --audio input.wav --output ./results --model medium

# Sử dụng GPU (nếu có)
python cli.py --audio input.wav --output ./results --device cuda
```

---

## 🔧 Tùy chỉnh Config

Chỉnh file `config.yaml`:

```yaml
# Model: tiny (nhanh) → large (chính xác)
stt:
  model: "medium"
  language: "vi"
  device: "cpu"  # hoặc "cuda" nếu có GPU

# Độ dài câu
sentence_splitter:
  min_length: 10
  max_length: 200

# Audio output
audio_segmentation:
  output_format: "wav"  # hoặc "mp3"
  output_sample_rate: 16000
```

---

## ⚙️ Model Size Comparison

| Model | RAM | Speed | Accuracy |
|-------|-----|-------|----------|
| tiny | ~1GB | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ |
| base | ~1GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ |
| small | ~2GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium | ~5GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| large | ~10GB | ⚡ | ⭐⭐⭐⭐⭐ |

**Khuyến nghị:**
- Máy thường: `base` hoặc `small`
- Máy mạnh: `medium`
- Cần độ chính xác cao: `large`
- Test nhanh: `tiny`

---

## 🎬 Video Tutorial

1. **Chuẩn bị audio** - File rõ ràng, ít noise
2. **Chọn model phù hợp** - Base/Small cho hầu hết trường hợp
3. **Chạy processing** - Đợi 1-5 phút tùy file
4. **Kiểm tra kết quả** - Mở folder output
5. **Chỉnh config nếu cần** - Tối ưu cho use case của bạn

---

## 🐛 Troubleshooting

### "FFmpeg not found"
```bash
# Cài FFmpeg và thêm vào PATH
# Windows: System Properties → Environment Variables → Path
# Linux/Mac: Thường tự động có trong PATH
```

### "CUDA not available"
```yaml
# config.yaml - đổi sang CPU
stt:
  device: "cpu"
```

### "Out of memory"
```yaml
# Dùng model nhỏ hơn
stt:
  model: "tiny"  # hoặc "base"
```

### Transcript không chính xác
- Dùng model lớn hơn (`medium` hoặc `large`)
- Kiểm tra chất lượng audio (16kHz+, mono, ít noise)
- Đảm bảo chọn đúng ngôn ngữ

### Câu bị tách sai
```yaml
# Chỉnh trong config.yaml
sentence_splitter:
  min_length: 20  # Tăng lên
  max_length: 150  # Giảm xuống
  merge_short_sentences: true
```

---

## 📊 Output Files Explained

### 1. segments/
Các file audio và text đã tách:
- `segment_0001.wav` - Audio của câu 1
- `segment_0001.txt` - Text của câu 1

### 2. full_transcript.txt
Toàn bộ text transcription

### 3. manifest.json
Metadata đầy đủ (timestamps, confidence, config)
```json
{
  "metadata": {...},
  "segments": [
    {
      "index": 0,
      "filename": "segment_0001.wav",
      "text": "...",
      "start": 0.0,
      "end": 2.5,
      "duration": 2.5
    }
  ]
}
```

### 4. metadata.csv
Dạng bảng, dễ import vào Excel/Sheets
```csv
index,filename,text,start,end,duration
0,segment_0001.wav,"...",0.0,2.5,2.5
```

---

## 🚀 Next Steps

Sau khi chạy thành công:

1. **Triển khai đa máy** → Xem `DEPLOYMENT.md`
2. **Tùy chỉnh nâng cao** → Xem `config.yaml` options
3. **Sử dụng API** → Xem `example.py`
4. **Tối ưu performance** → GPU, batch processing

---

## 💡 Tips

### Tối ưu tốc độ
- Dùng GPU: `device: "cuda"`
- Dùng faster-whisper: `engine: "faster-whisper"`
- Model nhỏ hơn: `model: "base"`

### Tối ưu chất lượng
- Model lớn: `model: "medium"` hoặc `"large"`
- Word timestamps: `word_timestamps: true`
- Optimize boundaries: `optimize_boundaries: true`

### Xử lý batch hiệu quả
```bash
# Tách files thành batch nhỏ
python cli.py --batch ./batch1 --output ./out &
python cli.py --batch ./batch2 --output ./out &
python cli.py --batch ./batch3 --output ./out &
```

---

## 📞 Need Help?

- **README.md** - Tổng quan và chi tiết
- **DEPLOYMENT.md** - Triển khai đa máy
- **config.yaml** - Các tùy chọn cấu hình
- **example.py** - Code examples

**Chúc bạn xử lý dữ liệu thành công! 🎉**
