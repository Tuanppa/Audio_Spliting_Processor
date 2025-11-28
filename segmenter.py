"""
Audio Segmenter Module - Cắt audio file thành các đoạn nhỏ theo timestamp
"""

from pathlib import Path
from typing import List, Tuple
import logging
from pydub import AudioSegment
from pydub.silence import detect_silence
import soundfile as sf

from config import AudioConfig
from transcriber import TranscriptSegment


class AudioSegmenter:
    """
    Class xử lý cắt audio file thành các đoạn nhỏ
    """
    
    def __init__(self, config: AudioConfig):
        """
        Khởi tạo AudioSegmenter
        
        Args:
            config: AudioConfig object
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def load_audio(self, audio_path: str) -> AudioSegment:
        """
        Load audio file
        
        Args:
            audio_path: Đường dẫn file audio
        
        Returns:
            AudioSegment object
        
        Supports: wav, mp3, flac, m4a, ogg, etc.
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.logger.info(f"Loading audio: {audio_path.name}")
        
        # Detect format từ extension
        format = audio_path.suffix[1:]  # Remove dot
        audio = AudioSegment.from_file(str(audio_path), format=format)
        
        # Resample nếu cần (Whisper yêu cầu 16kHz)
        if audio.frame_rate != self.config.sample_rate:
            self.logger.info(
                f"Resampling from {audio.frame_rate}Hz to {self.config.sample_rate}Hz"
            )
            audio = audio.set_frame_rate(self.config.sample_rate)
        
        # Convert to mono nếu là stereo
        if audio.channels > 1:
            self.logger.info("Converting to mono")
            audio = audio.set_channels(1)
        
        return audio
    
    def segment_audio(
        self, 
        audio: AudioSegment, 
        segments: List[TranscriptSegment]
    ) -> List[Tuple[AudioSegment, TranscriptSegment]]:
        """
        Cắt audio thành các đoạn theo timestamps
        
        Args:
            audio: AudioSegment object (toàn bộ audio)
            segments: List TranscriptSegment (chứa timestamp)
        
        Returns:
            List of (audio_segment, transcript_segment) tuples
        
        Process:
            1. Với mỗi TranscriptSegment, lấy thời gian start và end
            2. Cắt audio từ start -> end
            3. Thêm một chút padding để tránh cắt mất âm thanh
        """
        segmented_audios = []
        
        for seg in segments:
            # Convert thời gian từ giây sang milliseconds
            start_ms = int(seg.start * 1000)
            end_ms = int(seg.end * 1000)
            
            # Add padding để tránh cắt mất đầu/cuối
            padding_ms = self.config.keep_silence
            start_ms = max(0, start_ms - padding_ms)
            end_ms = min(len(audio), end_ms + padding_ms)
            
            # Cắt audio
            audio_segment = audio[start_ms:end_ms]
            
            segmented_audios.append((audio_segment, seg))
            
            self.logger.debug(
                f"Segment {seg.id}: {seg.start:.2f}s - {seg.end:.2f}s "
                f"({audio_segment.duration_seconds:.2f}s)"
            )
        
        self.logger.info(f"Segmented audio into {len(segmented_audios)} parts")
        return segmented_audios
    
    def export_segments(
        self,
        audio_path: str,
        segments: List[TranscriptSegment],
        output_dir: str,
        prefix: str = "segment",
        padding: int = 4
    ) -> List[Dict]:
        """
        Export các audio segments ra file riêng biệt
        
        Args:
            audio_path: Đường dẫn audio gốc
            segments: List TranscriptSegment
            output_dir: Thư mục output
            prefix: Tiền tố tên file
            padding: Số chữ số đệm (0001, 0002...)
        
        Returns:
            List dict chứa thông tin các file đã export
        
        Output structure:
            output_dir/
                segment_0001.wav
                segment_0001.txt
                segment_0002.wav
                segment_0002.txt
                ...
        """
        # Load audio
        audio = self.load_audio(audio_path)
        
        # Segment audio
        segmented_audios = self.segment_audio(audio, segments)
        
        # Tạo output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        exported_files = []
        
        for audio_seg, transcript_seg in segmented_audios:
            # Tạo tên file
            file_id = str(transcript_seg.id).zfill(padding)
            audio_filename = f"{prefix}_{file_id}.{self.config.format}"
            text_filename = f"{prefix}_{file_id}.txt"
            
            audio_path_out = output_dir / audio_filename
            text_path_out = output_dir / text_filename
            
            # Export audio
            audio_seg.export(
                str(audio_path_out),
                format=self.config.format,
                parameters=["-ar", str(self.config.sample_rate)]
            )
            
            # Export text
            with open(text_path_out, 'w', encoding='utf-8') as f:
                f.write(transcript_seg.text)
            
            # Lưu metadata
            exported_files.append({
                "id": transcript_seg.id,
                "audio_file": audio_filename,
                "text_file": text_filename,
                "text": transcript_seg.text,
                "start": transcript_seg.start,
                "end": transcript_seg.end,
                "duration": transcript_seg.duration
            })
            
            self.logger.debug(f"Exported: {audio_filename}")
        
        self.logger.info(
            f"Successfully exported {len(exported_files)} segments to {output_dir}"
        )
        
        return exported_files
    
    def detect_silence_segments(self, audio_path: str) -> List[Tuple[float, float]]:
        """
        Phát hiện các đoạn im lặng trong audio
        (Có thể dùng để split audio tự động nếu không có transcript)
        
        Args:
            audio_path: Đường dẫn audio
        
        Returns:
            List of (start, end) tuples in seconds
        """
        audio = self.load_audio(audio_path)
        
        # Detect silence
        silence_ranges = detect_silence(
            audio,
            min_silence_len=self.config.min_silence_len,
            silence_thresh=self.config.silence_thresh
        )
        
        # Convert từ milliseconds sang seconds
        silence_ranges_sec = [
            (start / 1000.0, end / 1000.0) 
            for start, end in silence_ranges
        ]
        
        self.logger.info(f"Detected {len(silence_ranges_sec)} silence segments")
        return silence_ranges_sec
    
    def export_manifest(
        self,
        exported_files: List[Dict],
        output_path: str
    ):
        """
        Tạo manifest file (JSON) chứa metadata của tất cả segments
        
        Args:
            exported_files: List dict từ export_segments()
            output_path: Đường dẫn file manifest JSON
        
        Format manifest:
            {
                "total_segments": 100,
                "total_duration": 3600.5,
                "segments": [...]
            }
        """
        import json
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        total_duration = sum(item["duration"] for item in exported_files)
        
        manifest = {
            "total_segments": len(exported_files),
            "total_duration": total_duration,
            "segments": exported_files
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Manifest saved to: {output_path}")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    from config import AudioConfig
    config = AudioConfig()
    
    segmenter = AudioSegmenter(config)
    
    # Test
    # segments = [...]  # từ transcriber
    # exported = segmenter.export_segments("input.wav", segments, "./output")
    # segmenter.export_manifest(exported, "./output/manifest.json")
