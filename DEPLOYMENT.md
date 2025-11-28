# Hướng dẫn Triển khai Đa Máy

## 📌 Tổng quan

Có 2 cách triển khai để sử dụng ứng dụng trên nhiều máy tính:

1. **Standalone Mode** - Mỗi máy chạy độc lập, chia sẻ kết quả qua folder chung
2. **Distributed Mode** - Sử dụng task queue để phân phối công việc

---

## 🔧 Option 1: Standalone Mode (Đơn giản)

### Ưu điểm
- Đơn giản, dễ setup
- Không cần server trung tâm
- Mỗi máy hoạt động độc lập

### Setup

#### Bước 1: Cài đặt trên mỗi máy

```bash
# Clone hoặc copy folder audio_processor lên mỗi máy
cd audio_processor

# Cài đặt dependencies
pip install -r requirements.txt

# Cài FFmpeg (nếu chưa có)
# Windows: choco install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# macOS: brew install ffmpeg
```

#### Bước 2: Setup folder chia sẻ

**Option A: Sử dụng Google Drive / Dropbox**

```yaml
# config.yaml - chỉnh output directory
output:
  default_dir: "D:/GoogleDrive/audio_processing_output"
  create_subfolder: true
  overwrite: false
```

**Option B: Sử dụng Network Share**

Windows:
```
# Map network drive
net use Z: \\server\shared_folder
```

Linux:
```bash
# Mount network share
sudo mount -t cifs //server/shared_folder /mnt/shared -o username=user
```

Cập nhật config.yaml:
```yaml
output:
  default_dir: "Z:/audio_processing_output"  # Windows
  # hoặc "/mnt/shared/audio_processing_output"  # Linux
```

#### Bước 3: Phân chia công việc

**Cách 1: Thủ công**
- Máy 1 xử lý file 1-10
- Máy 2 xử lý file 11-20
- ...

**Cách 2: Sử dụng naming convention**
```
input/
  ├── batch1/  → Máy 1 xử lý
  ├── batch2/  → Máy 2 xử lý
  └── batch3/  → Máy 3 xử lý
```

**Cách 3: Script tự động chia**

```python
# distribute_tasks.py
import os
import shutil

def distribute_files(input_dir, num_workers):
    files = [f for f in os.listdir(input_dir) if f.endswith(('.wav', '.mp3'))]
    
    for i, file in enumerate(files):
        worker_id = i % num_workers
        batch_dir = f"batch_{worker_id}"
        os.makedirs(batch_dir, exist_ok=True)
        shutil.copy(
            os.path.join(input_dir, file),
            os.path.join(batch_dir, file)
        )

distribute_files("./all_audio", num_workers=3)
```

#### Bước 4: Chạy trên mỗi máy

```bash
# Máy 1
python cli.py --batch batch_0 --output Z:/output

# Máy 2  
python cli.py --batch batch_1 --output Z:/output

# Máy 3
python cli.py --batch batch_2 --output Z:/output
```

---

## 🚀 Option 2: Distributed Mode (Nâng cao)

### Ưu điểm
- Tự động phân phối công việc
- Load balancing
- Tracking tiến độ tập trung
- Xử lý lỗi tốt hơn

### Kiến trúc

```
                 ┌─────────────┐
                 │   Master    │
                 │   Server    │
                 └──────┬──────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
     ┌────▼───┐    ┌────▼───┐    ┌────▼───┐
     │Worker 1│    │Worker 2│    │Worker 3│
     └────────┘    └────────┘    └────────┘
```

### Setup với Celery + Redis

#### Bước 1: Cài đặt dependencies

```bash
pip install celery redis
```

#### Bước 2: Tạo file tasks.py

```python
# tasks.py
from celery import Celery
import os
import yaml
from core import Transcriber, SentenceSplitter, Aligner, AudioCutter, Exporter

# Celery config
app = Celery('audio_processor', broker='redis://localhost:6379/0')

@app.task(bind=True)
def process_audio_task(self, audio_path, output_dir):
    """Celery task to process audio"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        # Initialize
        transcriber = Transcriber(config)
        sentence_splitter = SentenceSplitter(config)
        aligner = Aligner(config)
        audio_cutter = AudioCutter(config)
        exporter = Exporter(config)
        
        # Update progress
        self.update_state(state='TRANSCRIBING')
        transcription = transcriber.transcribe(audio_path)
        
        self.update_state(state='SPLITTING')
        sentences = sentence_splitter.split_sentences(
            transcription['text'],
            language=transcription['language']
        )
        
        self.update_state(state='ALIGNING')
        aligned = aligner.align_sentences(sentences, transcription)
        
        self.update_state(state='CUTTING')
        segments_dir = os.path.join(output_dir, "segments")
        segments = audio_cutter.cut_audio(audio_path, aligned, segments_dir)
        
        self.update_state(state='EXPORTING')
        exporter.export_all(
            segments,
            output_dir,
            os.path.basename(audio_path),
            transcription
        )
        
        return {
            'status': 'success',
            'segments': len(segments),
            'output': output_dir
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
```

#### Bước 3: Setup Redis Server

```bash
# Ubuntu
sudo apt install redis-server
sudo systemctl start redis

# Windows
# Download từ: https://github.com/microsoftarchive/redis/releases
# Chạy redis-server.exe

# macOS
brew install redis
brew services start redis
```

#### Bước 4: Chạy Master Server

```bash
# Trên máy master
redis-server  # Terminal 1

# Chạy Celery worker để monitor
celery -A tasks worker --loglevel=info  # Terminal 2
```

#### Bước 5: Chạy Workers trên các máy

```bash
# Trên mỗi máy worker
# Sửa broker URL trong tasks.py thành IP máy master
# broker='redis://192.168.1.100:6379/0'

celery -A tasks worker --loglevel=info --concurrency=1
```

#### Bước 6: Submit tasks

```python
# submit_jobs.py
from tasks import process_audio_task
import os

def submit_batch(input_dir, output_dir):
    """Submit all audio files as tasks"""
    
    audio_files = [
        f for f in os.listdir(input_dir)
        if f.endswith(('.wav', '.mp3', '.m4a'))
    ]
    
    tasks = []
    for audio_file in audio_files:
        audio_path = os.path.join(input_dir, audio_file)
        
        # Submit task
        task = process_audio_task.delay(audio_path, output_dir)
        tasks.append({
            'file': audio_file,
            'task_id': task.id
        })
        print(f"Submitted: {audio_file} - Task ID: {task.id}")
    
    return tasks

if __name__ == "__main__":
    tasks = submit_batch("./input", "./output")
    print(f"\nSubmitted {len(tasks)} tasks")
    
    # Track progress
    from celery.result import AsyncResult
    import time
    
    while True:
        completed = 0
        for task_info in tasks:
            result = AsyncResult(task_info['task_id'])
            if result.ready():
                completed += 1
        
        print(f"Progress: {completed}/{len(tasks)}")
        
        if completed == len(tasks):
            break
        
        time.sleep(5)
    
    print("All tasks completed!")
```

#### Bước 7: Monitor

```python
# monitor.py
from celery.result import AsyncResult
from tasks import app
import time

def monitor_tasks(task_ids):
    """Monitor task progress"""
    
    while True:
        states = {}
        for task_id in task_ids:
            result = AsyncResult(task_id)
            state = result.state
            states[state] = states.get(state, 0) + 1
        
        print("\nTask Status:")
        for state, count in states.items():
            print(f"  {state}: {count}")
        
        if all(AsyncResult(tid).ready() for tid in task_ids):
            break
        
        time.sleep(2)

# Usage
# task_ids = ['task-id-1', 'task-id-2', ...]
# monitor_tasks(task_ids)
```

---

## 📊 So sánh

| Tiêu chí | Standalone | Distributed |
|----------|-----------|------------|
| Độ phức tạp | ⭐ Đơn giản | ⭐⭐⭐ Phức tạp |
| Setup time | 10 phút | 30-60 phút |
| Cần server | ❌ Không | ✅ Cần Redis |
| Auto load-balance | ❌ | ✅ |
| Monitoring | Thủ công | Tự động |
| Fault tolerance | Thấp | Cao |
| Scalability | Thủ công | Tự động |

---

## 💡 Best Practices

### 1. Optimize cho Performance

**GPU Acceleration:**
```yaml
# config.yaml
stt:
  device: "cuda"  # Nếu có GPU
  compute_type: "float16"  # GPU mode
```

**Batch Processing:**
```bash
# Xử lý nhiều file cùng lúc
python cli.py --batch ./input --output ./output
```

### 2. Error Handling

```python
# Wrapper script với retry
import subprocess
import time

def process_with_retry(audio_file, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = subprocess.run([
                'python', 'cli.py',
                '--audio', audio_file,
                '--output', './output'
            ], check=True)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    return False
```

### 3. Resource Management

```yaml
# config.yaml - Giảm memory usage
processing:
  batch_size: 1
  num_workers: 1

stt:
  model: "base"  # Dùng model nhỏ hơn nếu RAM hạn chế
```

### 4. Progress Tracking

```python
# track_progress.py
import os
import json
from datetime import datetime

def log_progress(audio_file, status, output_file="progress.json"):
    """Log progress to file"""
    
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            data = json.load(f)
    else:
        data = []
    
    data.append({
        'file': audio_file,
        'status': status,
        'timestamp': datetime.now().isoformat()
    })
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
```

---

## 🔍 Troubleshooting

### Issue: Worker không kết nối được Redis

```bash
# Kiểm tra Redis
redis-cli ping  # Should return PONG

# Kiểm tra firewall
sudo ufw allow 6379  # Ubuntu
```

### Issue: Out of memory

```yaml
# Giảm model size
stt:
  model: "tiny"  # hoặc "base"

# Hoặc tắt word timestamps
stt:
  word_timestamps: false
```

### Issue: File conflict khi nhiều máy ghi cùng folder

```python
# Thêm machine ID vào filename
import socket

machine_id = socket.gethostname()
naming_pattern = f"{machine_id}_segment_{{index:04d}}"
```

---

## 📞 Support

Nếu cần hỗ trợ thêm về triển khai, hãy tham khảo:
- README.md - Hướng dẫn cơ bản
- config.yaml - Các tùy chọn cấu hình
- Source code - Chi tiết implementation
