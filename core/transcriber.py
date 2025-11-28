"""
Audio to Text Transcription Module
Sử dụng Whisper/Faster-Whisper để chuyển audio thành text với timestamps
"""

import os
import warnings
from typing import Dict, List, Optional, Tuple
import numpy as np

# Suppress warnings
warnings.filterwarnings("ignore")


class Transcriber:
    """Chuyển audio thành text với timestamps chi tiết"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self.engine = config['stt']['engine']
        self.model_size = config['stt']['model']
        self.language = config['stt']['language']
        self.device = config['stt']['device']
        
        self._load_model()
    
    def _load_model(self):
        """Load model Whisper hoặc Faster-Whisper"""
        print(f"Loading {self.engine} model: {self.model_size}...")
        
        if self.engine == "faster-whisper":
            from faster_whisper import WhisperModel
            
            compute_type = self.config['stt'].get('compute_type', 'int8')
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=compute_type
            )
            print(f"✓ Faster-Whisper model loaded (compute_type: {compute_type})")
            
        else:  # whisper
            import whisper
            
            self.model = whisper.load_model(self.model_size, device=self.device)
            print(f"✓ Whisper model loaded")
    
    def transcribe(self, audio_path: str) -> Dict:
        """
        Chuyển audio thành text với timestamps
        
        Args:
            audio_path: Đường dẫn file audio
            
        Returns:
            Dict chứa:
            - text: Full transcript
            - segments: List các segment với timestamps
            - language: Ngôn ngữ phát hiện được
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"\nTranscribing: {os.path.basename(audio_path)}")
        
        if self.engine == "faster-whisper":
            return self._transcribe_faster_whisper(audio_path)
        else:
            return self._transcribe_whisper(audio_path)
    
    def _transcribe_faster_whisper(self, audio_path: str) -> Dict:
        """Transcribe using Faster-Whisper"""
        language = None if self.language == "auto" else self.language
        word_timestamps = self.config['stt'].get('word_timestamps', True)
        
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            word_timestamps=word_timestamps,
            beam_size=5,
            vad_filter=True,  # Voice Activity Detection
            vad_parameters=dict(
                threshold=0.5,
                min_speech_duration_ms=250,
                min_silence_duration_ms=100
            )
        )
        
        # Convert segments to list and extract info
        result_segments = []
        full_text = []
        
        for segment in segments:
            seg_dict = {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
                'confidence': getattr(segment, 'avg_logprob', None)
            }
            
            # Thêm word-level timestamps nếu có
            if word_timestamps and hasattr(segment, 'words'):
                seg_dict['words'] = [
                    {
                        'word': word.word,
                        'start': word.start,
                        'end': word.end,
                        'probability': word.probability
                    }
                    for word in segment.words
                ]
            
            result_segments.append(seg_dict)
            full_text.append(segment.text.strip())
        
        return {
            'text': ' '.join(full_text),
            'segments': result_segments,
            'language': info.language,
            'duration': info.duration
        }
    
    def _transcribe_whisper(self, audio_path: str) -> Dict:
        """Transcribe using standard Whisper"""
        import whisper
        
        language = None if self.language == "auto" else self.language
        word_timestamps = self.config['stt'].get('word_timestamps', True)
        
        result = self.model.transcribe(
            audio_path,
            language=language,
            word_timestamps=word_timestamps,
            verbose=False
        )
        
        # Format segments
        result_segments = []
        for segment in result['segments']:
            seg_dict = {
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip(),
                'confidence': segment.get('avg_logprob', None)
            }
            
            # Add word-level timestamps if available
            if 'words' in segment:
                seg_dict['words'] = segment['words']
            
            result_segments.append(seg_dict)
        
        return {
            'text': result['text'],
            'segments': result_segments,
            'language': result['language'],
            'duration': None  # Whisper doesn't provide duration directly
        }
    
    def get_words_with_timestamps(self, transcription: Dict) -> List[Dict]:
        """
        Trích xuất tất cả các từ với timestamps từ transcription
        
        Returns:
            List of {word, start, end}
        """
        words = []
        
        for segment in transcription['segments']:
            if 'words' in segment:
                for word_info in segment['words']:
                    words.append({
                        'word': word_info['word'].strip(),
                        'start': word_info['start'],
                        'end': word_info['end']
                    })
        
        return words


def test_transcriber():
    """Test function"""
    config = {
        'stt': {
            'model': 'base',
            'engine': 'faster-whisper',
            'language': 'vi',
            'device': 'cpu',
            'compute_type': 'int8',
            'word_timestamps': True
        }
    }
    
    transcriber = Transcriber(config)
    
    # Test với file audio mẫu (cần có file thật để test)
    # result = transcriber.transcribe("sample.wav")
    # print(result['text'])
    print("Transcriber module ready!")


if __name__ == "__main__":
    test_transcriber()
