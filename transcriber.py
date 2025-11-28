"""
Transcriber Module - Sử dụng Whisper để chuyển audio thành text có timestamp
"""

import whisper
import stable_whisper
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

from config import WhisperConfig


@dataclass
class TranscriptSegment:
    """
    Một đoạn transcript với thông tin chi tiết
    """
    id: int
    start: float  # Thời gian bắt đầu (giây)
    end: float    # Thời gian kết thúc (giây)
    text: str     # Nội dung text
    
    @property
    def duration(self) -> float:
        """Độ dài của segment (giây)"""
        return self.end - self.start
    
    def to_dict(self) -> Dict:
        """Convert sang dictionary"""
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "text": self.text,
            "duration": self.duration
        }


class AudioTranscriber:
    """
    Class xử lý transcription audio thành text sử dụng Whisper
    """
    
    def __init__(self, config: WhisperConfig):
        """
        Khởi tạo transcriber
        
        Args:
            config: WhisperConfig object chứa cấu hình Whisper
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load Whisper model
        self.logger.info(f"Loading Whisper model: {config.model_size} on {config.device}")
        self.model = stable_whisper.load_model(
            config.model_size,
            device=config.device
        )
        self.logger.info("Model loaded successfully")
    
    def transcribe(self, audio_path: str) -> List[TranscriptSegment]:
        """
        Transcribe audio file thành text với timestamp
        
        Args:
            audio_path: Đường dẫn tới file audio
        
        Returns:
            List các TranscriptSegment
        
        Process:
            1. Load audio file
            2. Chạy Whisper để nhận diện giọng nói
            3. Stable-ts tự động align timestamp cho từng từ
            4. Split thành các segment theo câu
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        self.logger.info(f"Transcribing: {audio_path.name}")
        
        # Transcribe với stable-whisper để có timestamp chính xác
        result = self.model.transcribe(
            str(audio_path),
            language=self.config.language,
            task=self.config.task,
            vad=self.config.vad,  # Voice Activity Detection
            mel_first=self.config.mel_first,
            word_timestamps=True  # Quan trọng: lấy timestamp từng từ
        )
        
        # Convert result thành list TranscriptSegment
        segments = []
        for idx, segment in enumerate(result.segments):
            segments.append(TranscriptSegment(
                id=idx,
                start=segment.start,
                end=segment.end,
                text=segment.text.strip()
            ))
        
        self.logger.info(f"Transcription complete: {len(segments)} segments found")
        return segments
    
    def transcribe_to_sentences(
        self, 
        audio_path: str,
        min_duration: float = 0.5,
        max_duration: float = 30.0
    ) -> List[TranscriptSegment]:
        """
        Transcribe và merge các segment thành câu hoàn chỉnh
        
        Args:
            audio_path: Đường dẫn audio
            min_duration: Thời lượng tối thiểu của một segment (giây)
            max_duration: Thời lượng tối đa của một segment (giây)
        
        Returns:
            List TranscriptSegment đã được merge thành câu
        
        Logic:
            - Whisper trả về segments (thường là phrase/clause)
            - Function này merge các segment ngắn thành câu dài hơn
            - Đảm bảo mỗi segment có độ dài hợp lý
        """
        segments = self.transcribe(audio_path)
        
        if not segments:
            return []
        
        merged_segments = []
        current_segment = segments[0]
        
        for next_segment in segments[1:]:
            # Kiểm tra nếu merge segment hiện tại với segment tiếp theo
            potential_duration = next_segment.end - current_segment.start
            
            # Merge nếu:
            # 1. Current segment quá ngắn
            # 2. Merge không vượt quá max_duration
            # 3. Text không kết thúc bằng dấu câu mạnh (. ! ?)
            should_merge = (
                current_segment.duration < min_duration or
                not current_segment.text.rstrip().endswith(('.', '!', '?'))
            ) and potential_duration <= max_duration
            
            if should_merge:
                # Merge: cập nhật thời gian kết thúc và nối text
                current_segment = TranscriptSegment(
                    id=current_segment.id,
                    start=current_segment.start,
                    end=next_segment.end,
                    text=current_segment.text + " " + next_segment.text
                )
            else:
                # Không merge: lưu segment hiện tại và bắt đầu segment mới
                merged_segments.append(current_segment)
                current_segment = next_segment
        
        # Thêm segment cuối cùng
        merged_segments.append(current_segment)
        
        # Re-index segments
        for idx, seg in enumerate(merged_segments):
            seg.id = idx
        
        self.logger.info(
            f"Merged into {len(merged_segments)} sentences "
            f"(original: {len(segments)} segments)"
        )
        
        return merged_segments
    
    def save_transcript(self, segments: List[TranscriptSegment], output_path: str):
        """
        Lưu transcript ra file text
        
        Args:
            segments: List TranscriptSegment
            output_path: Đường dẫn file output
        
        Format:
            [0.00 - 3.45] This is the first sentence.
            [3.45 - 7.89] This is the second sentence.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in segments:
                f.write(f"[{seg.start:.2f} - {seg.end:.2f}] {seg.text}\n")
        
        self.logger.info(f"Transcript saved to: {output_path}")
    
    def save_transcript_json(self, segments: List[TranscriptSegment], output_path: str):
        """
        Lưu transcript dạng JSON
        
        Args:
            segments: List TranscriptSegment
            output_path: Đường dẫn file JSON
        """
        import json
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "segments": [seg.to_dict() for seg in segments],
            "total_segments": len(segments),
            "total_duration": segments[-1].end if segments else 0
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"JSON transcript saved to: {output_path}")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Khởi tạo config
    from config import WhisperConfig
    config = WhisperConfig(model_size="base", device="cpu")
    
    # Tạo transcriber
    transcriber = AudioTranscriber(config)
    
    # Test với file audio mẫu
    # segments = transcriber.transcribe_to_sentences("sample.wav")
    # transcriber.save_transcript(segments, "output.txt")
