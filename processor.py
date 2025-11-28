"""
Audio Processor - Module chính điều phối toàn bộ workflow
"""

from pathlib import Path
from typing import List, Optional
import logging
import json
from datetime import datetime

from config import AppConfig
from transcriber import AudioTranscriber, TranscriptSegment
from segmenter import AudioSegmenter


class AudioProcessor:
    """
    Main processor orchestrating the entire workflow:
    Audio → Transcribe → Segment → Export
    """
    
    def __init__(self, config: AppConfig):
        """
        Khởi tạo processor với configuration
        
        Args:
            config: AppConfig object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Tạo các thư mục cần thiết
        self.config.paths.create_directories()
        
        # Khởi tạo các sub-components
        self.transcriber = AudioTranscriber(self.config.whisper)
        self.segmenter = AudioSegmenter(self.config.audio)
        
        self.logger.info("AudioProcessor initialized")
    
    def process_single_file(
        self, 
        audio_path: str,
        output_dir: Optional[str] = None
    ) -> dict:
        """
        Xử lý một file audio duy nhất
        
        Args:
            audio_path: Đường dẫn tới file audio input
            output_dir: Thư mục output (nếu None, dùng config default)
        
        Returns:
            Dictionary chứa kết quả và metadata
        
        Workflow:
            1. Transcribe audio → text với timestamps
            2. Merge segments thành câu hoàn chỉnh
            3. Cắt audio theo timestamps
            4. Export segments ra file
            5. Tạo manifest file
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Setup output directory
        if output_dir is None:
            output_dir = self.config.paths.output_dir / audio_path.stem
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Processing: {audio_path.name}")
        self.logger.info(f"Output dir: {output_dir}")
        self.logger.info(f"{'='*60}\n")
        
        # Step 1: Transcribe
        self.logger.info("Step 1/4: Transcribing audio...")
        segments = self.transcriber.transcribe_to_sentences(
            str(audio_path),
            min_duration=self.config.audio.min_segment_duration,
            max_duration=self.config.audio.max_segment_duration
        )
        
        if not segments:
            self.logger.warning("No speech detected in audio")
            return {
                "status": "failed",
                "reason": "No speech detected",
                "segments": 0
            }
        
        # Step 2: Save full transcript
        self.logger.info("Step 2/4: Saving transcript...")
        transcript_path = output_dir / "full_transcript.txt"
        transcript_json_path = output_dir / "full_transcript.json"
        
        self.transcriber.save_transcript(segments, str(transcript_path))
        self.transcriber.save_transcript_json(segments, str(transcript_json_path))
        
        # Step 3: Segment and export audio
        self.logger.info("Step 3/4: Segmenting and exporting audio...")
        exported_files = self.segmenter.export_segments(
            audio_path=str(audio_path),
            segments=segments,
            output_dir=str(output_dir),
            prefix=self.config.process.prefix,
            padding=self.config.process.padding
        )
        
        # Step 4: Create manifest
        self.logger.info("Step 4/4: Creating manifest...")
        manifest_path = output_dir / "manifest.json"
        self.segmenter.export_manifest(exported_files, str(manifest_path))
        
        # Create processing metadata
        metadata = {
            "status": "success",
            "input_file": str(audio_path),
            "output_dir": str(output_dir),
            "total_segments": len(segments),
            "total_duration": segments[-1].end if segments else 0,
            "processed_at": datetime.now().isoformat(),
            "config": {
                "whisper_model": self.config.whisper.model_size,
                "sample_rate": self.config.audio.sample_rate,
                "format": self.config.audio.format
            }
        }
        
        # Save metadata
        metadata_path = output_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"✓ Processing complete!")
        self.logger.info(f"  - Segments: {len(segments)}")
        self.logger.info(f"  - Duration: {segments[-1].end:.2f}s")
        self.logger.info(f"  - Output: {output_dir}")
        self.logger.info(f"{'='*60}\n")
        
        return metadata
    
    def process_batch(
        self,
        input_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
        extensions: List[str] = [".wav", ".mp3", ".flac", ".m4a"]
    ) -> List[dict]:
        """
        Xử lý batch nhiều file audio trong một thư mục
        
        Args:
            input_dir: Thư mục chứa audio files (nếu None, dùng config)
            output_dir: Thư mục output (nếu None, dùng config)
            extensions: Danh sách extension được hỗ trợ
        
        Returns:
            List metadata của tất cả files đã xử lý
        """
        if input_dir is None:
            input_dir = self.config.paths.input_dir
        else:
            input_dir = Path(input_dir)
        
        if output_dir is None:
            output_dir = self.config.paths.output_dir
        else:
            output_dir = Path(output_dir)
        
        # Tìm tất cả audio files
        audio_files = []
        for ext in extensions:
            audio_files.extend(input_dir.glob(f"*{ext}"))
            audio_files.extend(input_dir.glob(f"*{ext.upper()}"))
        
        audio_files = sorted(set(audio_files))
        
        if not audio_files:
            self.logger.warning(f"No audio files found in {input_dir}")
            return []
        
        self.logger.info(f"Found {len(audio_files)} audio files to process")
        
        # Process each file
        results = []
        for idx, audio_file in enumerate(audio_files, 1):
            self.logger.info(f"\nProcessing file {idx}/{len(audio_files)}")
            
            try:
                # Tạo output dir riêng cho mỗi file
                file_output_dir = output_dir / audio_file.stem
                
                result = self.process_single_file(
                    str(audio_file),
                    str(file_output_dir)
                )
                results.append(result)
                
            except Exception as e:
                self.logger.error(f"Failed to process {audio_file.name}: {e}")
                results.append({
                    "status": "failed",
                    "input_file": str(audio_file),
                    "error": str(e)
                })
        
        # Save batch summary
        summary_path = output_dir / "batch_summary.json"
        with open(summary_path, 'w') as f:
            json.dump({
                "total_files": len(audio_files),
                "successful": sum(1 for r in results if r["status"] == "success"),
                "failed": sum(1 for r in results if r["status"] == "failed"),
                "results": results,
                "processed_at": datetime.now().isoformat()
            }, f, indent=2)
        
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Batch processing complete!")
        self.logger.info(f"  - Total files: {len(audio_files)}")
        self.logger.info(f"  - Successful: {sum(1 for r in results if r['status'] == 'success')}")
        self.logger.info(f"  - Failed: {sum(1 for r in results if r['status'] == 'failed')}")
        self.logger.info(f"  - Summary: {summary_path}")
        self.logger.info(f"{'='*60}\n")
        
        return results
    
    def get_processing_stats(self, output_dir: str) -> dict:
        """
        Tính toán thống kê từ một output directory
        
        Args:
            output_dir: Thư mục chứa kết quả đã xử lý
        
        Returns:
            Dictionary chứa thống kê
        """
        output_dir = Path(output_dir)
        
        if not output_dir.exists():
            return {"error": "Directory not found"}
        
        # Load manifest
        manifest_path = output_dir / "manifest.json"
        if not manifest_path.exists():
            return {"error": "Manifest not found"}
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        segments = manifest["segments"]
        
        stats = {
            "total_segments": len(segments),
            "total_duration": manifest["total_duration"],
            "avg_segment_duration": manifest["total_duration"] / len(segments) if segments else 0,
            "shortest_segment": min(s["duration"] for s in segments) if segments else 0,
            "longest_segment": max(s["duration"] for s in segments) if segments else 0,
            "total_words": sum(len(s["text"].split()) for s in segments),
            "avg_words_per_segment": sum(len(s["text"].split()) for s in segments) / len(segments) if segments else 0
        }
        
        return stats


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    from config import AppConfig
    config = AppConfig()
    
    # Create processor
    processor = AudioProcessor(config)
    
    # Process single file
    # result = processor.process_single_file("sample.wav")
    
    # Or process batch
    # results = processor.process_batch()
