"""
Configuration file for Audio Processor
Chứa các cài đặt mặc định cho toàn bộ hệ thống
"""

from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal


class WhisperConfig(BaseModel):
    """Cấu hình cho Whisper model"""
    model_size: Literal["tiny", "base", "small", "medium", "large"] = "base"
    # tiny: nhanh nhất, kém chính xác nhất
    # base: cân bằng tốc độ và độ chính xác
    # small: chính xác hơn base
    # medium: rất chính xác nhưng chậm
    # large: chính xác nhất nhưng cần GPU mạnh
    
    device: Literal["cuda", "cpu"] = "cpu"  # Dùng "cuda" nếu có GPU
    language: str = "en"  # English
    task: Literal["transcribe", "translate"] = "transcribe"
    
    # Stable-ts settings for better alignment
    vad: bool = True  # Voice Activity Detection - phát hiện vùng có giọng nói
    mel_first: bool = True  # Tối ưu hóa alignment
    
    
class AudioConfig(BaseModel):
    """Cấu hình xử lý audio"""
    sample_rate: int = 16000  # Whisper yêu cầu 16kHz
    format: str = "wav"  # Định dạng output
    min_silence_len: int = 500  # ms - độ dài tối thiểu của khoảng lặng
    silence_thresh: int = -40  # dB - ngưỡng coi là im lặng
    keep_silence: int = 200  # ms - giữ lại một ít silence ở đầu/cuối
    
    # Minimum segment duration
    min_segment_duration: float = 0.5  # seconds - đoạn audio tối thiểu 0.5s
    max_segment_duration: float = 30.0  # seconds - đoạn audio tối đa 30s
    

class ProcessConfig(BaseModel):
    """Cấu hình xử lý"""
    output_format: Literal["individual", "manifest", "both"] = "both"
    # individual: mỗi câu 1 file audio + 1 file text
    # manifest: 1 file JSON chứa tất cả metadata
    # both: cả hai cách trên
    
    batch_size: int = 1  # Số file xử lý cùng lúc (cho đa luồng)
    num_workers: int = 1  # Số worker threads
    
    # Naming convention
    prefix: str = "segment"  # Tiền tố tên file: segment_0001.wav
    padding: int = 4  # Số chữ số: 0001, 0002...
    

class PathConfig(BaseModel):
    """Cấu hình đường dẫn"""
    input_dir: Path = Field(default_factory=lambda: Path("./input"))
    output_dir: Path = Field(default_factory=lambda: Path("./output"))
    temp_dir: Path = Field(default_factory=lambda: Path("./temp"))
    
    def create_directories(self):
        """Tạo các thư mục nếu chưa tồn tại"""
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)


class AppConfig(BaseModel):
    """Cấu hình tổng thể của ứng dụng"""
    whisper: WhisperConfig = Field(default_factory=WhisperConfig)
    audio: AudioConfig = Field(default_factory=AudioConfig)
    process: ProcessConfig = Field(default_factory=ProcessConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    
    # Logging
    verbose: bool = True  # In ra thông tin chi tiết
    log_file: str = "audio_processor.log"
    

# Khởi tạo config mặc định
DEFAULT_CONFIG = AppConfig()


def load_config(config_path: str = None) -> AppConfig:
    """
    Load configuration từ file hoặc dùng mặc định
    
    Args:
        config_path: Đường dẫn tới file config JSON (optional)
    
    Returns:
        AppConfig object
    """
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            import json
            data = json.load(f)
            return AppConfig(**data)
    return DEFAULT_CONFIG


def save_config(config: AppConfig, config_path: str):
    """
    Lưu configuration ra file
    
    Args:
        config: AppConfig object
        config_path: Đường dẫn lưu file
    """
    with open(config_path, 'w') as f:
        import json
        json.dump(config.model_dump(), f, indent=2, default=str)
