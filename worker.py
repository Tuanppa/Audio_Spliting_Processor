"""
Worker Script - Để triển khai trên nhiều máy tính
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Optional
import json
from datetime import datetime

from config import AppConfig
from processor import AudioProcessor


class Worker:
    """
    Worker class để xử lý audio trên nhiều máy
    
    Workflow:
        1. Worker monitor một shared input directory (có thể là network drive)
        2. Pick up file chưa được xử lý
        3. Lock file (tạo .processing file)
        4. Process file
        5. Move kết quả ra shared output directory
        6. Đánh dấu hoàn thành
    """
    
    def __init__(
        self,
        worker_id: str,
        shared_input_dir: str,
        shared_output_dir: str,
        config: AppConfig
    ):
        """
        Khởi tạo Worker
        
        Args:
            worker_id: ID của worker này (ví dụ: "worker_01")
            shared_input_dir: Thư mục chung chứa audio cần xử lý
            shared_output_dir: Thư mục chung để lưu kết quả
            config: AppConfig
        """
        self.worker_id = worker_id
        self.shared_input_dir = Path(shared_input_dir)
        self.shared_output_dir = Path(shared_output_dir)
        self.config = config
        
        self.logger = logging.getLogger(f"Worker-{worker_id}")
        
        # Tạo thư mục
        self.shared_input_dir.mkdir(parents=True, exist_ok=True)
        self.shared_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize processor
        self.processor = AudioProcessor(config)
        
        self.logger.info(f"Worker {worker_id} initialized")
        self.logger.info(f"  Input dir: {shared_input_dir}")
        self.logger.info(f"  Output dir: {shared_output_dir}")
    
    def get_pending_files(self) -> list:
        """
        Tìm các file audio chưa được xử lý
        
        Returns:
            List các Path object
        
        Logic:
            - File chưa xử lý: không có .processing và không có .done
            - File đang xử lý: có .processing
            - File đã xử lý: có .done
        """
        extensions = [".wav", ".mp3", ".flac", ".m4a", ".ogg"]
        
        pending_files = []
        
        for ext in extensions:
            for audio_file in self.shared_input_dir.glob(f"*{ext}"):
                processing_marker = audio_file.with_suffix(audio_file.suffix + ".processing")
                done_marker = audio_file.with_suffix(audio_file.suffix + ".done")
                
                # Chỉ lấy file chưa được xử lý
                if not processing_marker.exists() and not done_marker.exists():
                    pending_files.append(audio_file)
        
        return sorted(pending_files)
    
    def lock_file(self, audio_file: Path) -> bool:
        """
        Lock file để worker khác không xử lý
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            True nếu lock thành công, False nếu file đã bị lock
        
        Mechanism:
            Tạo file .processing chứa worker_id và timestamp
        """
        lock_file = audio_file.with_suffix(audio_file.suffix + ".processing")
        
        # Check nếu file đã bị lock (race condition)
        if lock_file.exists():
            return False
        
        try:
            # Atomic write
            lock_data = {
                "worker_id": self.worker_id,
                "locked_at": datetime.now().isoformat(),
                "file": str(audio_file)
            }
            
            with open(lock_file, 'w') as f:
                json.dump(lock_data, f, indent=2)
            
            self.logger.info(f"Locked file: {audio_file.name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to lock file: {e}")
            return False
    
    def unlock_file(self, audio_file: Path):
        """
        Unlock file và đánh dấu đã hoàn thành
        
        Args:
            audio_file: Path to audio file
        """
        lock_file = audio_file.with_suffix(audio_file.suffix + ".processing")
        done_file = audio_file.with_suffix(audio_file.suffix + ".done")
        
        # Remove lock
        if lock_file.exists():
            lock_file.unlink()
        
        # Create done marker
        done_data = {
            "worker_id": self.worker_id,
            "completed_at": datetime.now().isoformat(),
            "file": str(audio_file)
        }
        
        with open(done_file, 'w') as f:
            json.dump(done_data, f, indent=2)
        
        self.logger.info(f"Marked as done: {audio_file.name}")
    
    def process_file(self, audio_file: Path) -> bool:
        """
        Xử lý một file audio
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        try:
            # Tạo output directory cho file này
            output_dir = self.shared_output_dir / audio_file.stem
            
            # Process
            result = self.processor.process_single_file(
                str(audio_file),
                str(output_dir)
            )
            
            return result["status"] == "success"
        
        except Exception as e:
            self.logger.error(f"Failed to process {audio_file.name}: {e}")
            return False
    
    def run(self, poll_interval: int = 10, max_files: Optional[int] = None):
        """
        Chạy worker loop
        
        Args:
            poll_interval: Thời gian chờ giữa các lần kiểm tra (giây)
            max_files: Số file tối đa xử lý (None = không giới hạn)
        
        Workflow:
            1. Scan shared directory để tìm file mới
            2. Lock và xử lý file
            3. Lưu kết quả
            4. Lặp lại
        """
        self.logger.info(f"Worker {self.worker_id} starting...")
        self.logger.info(f"Poll interval: {poll_interval}s")
        
        processed_count = 0
        
        try:
            while True:
                # Tìm file pending
                pending_files = self.get_pending_files()
                
                if pending_files:
                    self.logger.info(f"Found {len(pending_files)} pending files")
                    
                    # Process first file
                    audio_file = pending_files[0]
                    
                    # Try to lock
                    if self.lock_file(audio_file):
                        self.logger.info(f"Processing: {audio_file.name}")
                        
                        # Process file
                        success = self.process_file(audio_file)
                        
                        if success:
                            self.logger.info(f"✓ Completed: {audio_file.name}")
                            processed_count += 1
                        else:
                            self.logger.error(f"✗ Failed: {audio_file.name}")
                        
                        # Unlock file
                        self.unlock_file(audio_file)
                        
                        # Check max_files limit
                        if max_files and processed_count >= max_files:
                            self.logger.info(f"Reached max files limit: {max_files}")
                            break
                    
                    else:
                        self.logger.debug(f"File already locked: {audio_file.name}")
                
                else:
                    self.logger.info("No pending files, waiting...")
                    time.sleep(poll_interval)
        
        except KeyboardInterrupt:
            self.logger.info("Worker stopped by user")
        
        except Exception as e:
            self.logger.error(f"Worker error: {e}", exc_info=True)
        
        finally:
            self.logger.info(f"Worker {self.worker_id} finished")
            self.logger.info(f"Total files processed: {processed_count}")


def main():
    """
    Main entry point cho worker
    """
    parser = argparse.ArgumentParser(
        description='Audio Processor Worker - Distributed processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Chạy worker trên máy 1
  python worker.py --id worker_01 --input /shared/input --output /shared/output
  
  # Chạy worker trên máy 2 với GPU
  python worker.py --id worker_02 --input /shared/input --output /shared/output --device cuda
  
  # Chạy worker xử lý tối đa 10 files rồi dừng
  python worker.py --id worker_03 --input /shared/input --output /shared/output --max-files 10
        """
    )
    
    # Worker configuration
    parser.add_argument(
        '--id',
        type=str,
        required=True,
        help='Worker ID (e.g., worker_01, worker_02)'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Shared input directory (network drive)'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Shared output directory (network drive)'
    )
    
    # Processing options
    parser.add_argument(
        '--model',
        type=str,
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base',
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--device',
        type=str,
        choices=['cpu', 'cuda'],
        default='cpu',
        help='Device (default: cpu)'
    )
    parser.add_argument(
        '--poll-interval',
        type=int,
        default=10,
        help='Polling interval in seconds (default: 10)'
    )
    parser.add_argument(
        '--max-files',
        type=int,
        help='Maximum files to process before stopping'
    )
    
    # Logging
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose logging'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    # Create config
    from config import AppConfig, WhisperConfig
    config = AppConfig(
        whisper=WhisperConfig(
            model_size=args.model,
            device=args.device
        )
    )
    
    # Create and run worker
    worker = Worker(
        worker_id=args.id,
        shared_input_dir=args.input,
        shared_output_dir=args.output,
        config=config
    )
    
    worker.run(
        poll_interval=args.poll_interval,
        max_files=args.max_files
    )


if __name__ == "__main__":
    main()
