"""
Audio Cutting Module
Cắt file audio thành các segments theo timestamps
"""

import os
from typing import List, Dict
from pydub import AudioSegment
from pydub.silence import detect_silence
import soundfile as sf
import numpy as np


class AudioCutter:
    """Cắt audio thành các segments"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.padding_before = config['audio_segmentation']['padding_before']
        self.padding_after = config['audio_segmentation']['padding_after']
        self.min_duration = config['audio_segmentation']['min_duration']
        self.max_duration = config['audio_segmentation']['max_duration']
        self.output_sample_rate = config['audio_segmentation'].get('output_sample_rate')
        self.output_format = config['audio_segmentation']['output_format']
        self.output_channels = config['audio_segmentation']['output_channels']
    
    def cut_audio(
        self,
        audio_path: str,
        aligned_sentences: List[Dict],
        output_dir: str
    ) -> List[Dict]:
        """
        Cắt audio thành các segments theo aligned_sentences
        
        Args:
            audio_path: Đường dẫn file audio gốc
            aligned_sentences: List các câu với timestamps
            output_dir: Thư mục output
            
        Returns:
            List các segment info với đường dẫn file
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Tạo output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Load audio
        print(f"Loading audio: {os.path.basename(audio_path)}")
        audio = AudioSegment.from_file(audio_path)
        
        # Get audio info
        original_sample_rate = audio.frame_rate
        original_channels = audio.channels
        
        print(f"Audio info: {original_sample_rate}Hz, {original_channels} channel(s), "
              f"{len(audio)/1000:.2f}s")
        
        # Process each segment
        segments_info = []
        
        for i, sentence_info in enumerate(aligned_sentences):
            segment_info = self._cut_segment(
                audio,
                sentence_info,
                i,
                output_dir,
                original_sample_rate
            )
            
            if segment_info:
                segments_info.append(segment_info)
        
        print(f"✓ Cut {len(segments_info)} segments to: {output_dir}")
        
        return segments_info
    
    def _cut_segment(
        self,
        audio: AudioSegment,
        sentence_info: Dict,
        index: int,
        output_dir: str,
        original_sample_rate: int
    ) -> Dict:
        """Cắt một segment từ audio"""
        
        # Lấy timestamps
        start = sentence_info['start']
        end = sentence_info['end']
        
        # Apply padding
        start_with_padding = max(0, start - self.padding_before)
        end_with_padding = min(len(audio) / 1000, end + self.padding_after)
        
        # Check duration
        duration = end_with_padding - start_with_padding
        
        if duration < self.min_duration:
            print(f"Warning: Segment {index} too short ({duration:.2f}s), skipping")
            return None
        
        if duration > self.max_duration:
            print(f"Warning: Segment {index} too long ({duration:.2f}s), truncating")
            end_with_padding = start_with_padding + self.max_duration
        
        # Convert to milliseconds for pydub
        start_ms = int(start_with_padding * 1000)
        end_ms = int(end_with_padding * 1000)
        
        # Extract segment
        segment = audio[start_ms:end_ms]
        
        # Convert to mono if needed
        if self.output_channels == 1 and segment.channels > 1:
            segment = segment.set_channels(1)
        
        # Resample if needed
        if self.output_sample_rate and segment.frame_rate != self.output_sample_rate:
            segment = segment.set_frame_rate(self.output_sample_rate)
        
        # Generate filename
        naming_pattern = self.config['export']['naming_pattern']
        filename = naming_pattern.format(index=index+1, name="segment")
        filename = f"{filename}.{self.output_format}"
        
        output_path = os.path.join(output_dir, filename)
        
        # Export
        segment.export(
            output_path,
            format=self.output_format,
            bitrate="128k" if self.output_format == "mp3" else None
        )
        
        return {
            'index': index,
            'filename': filename,
            'path': output_path,
            'text': sentence_info['text'],
            'start': start,
            'end': end,
            'duration': duration,
            'sample_rate': segment.frame_rate,
            'channels': segment.channels,
            'confidence': sentence_info.get('confidence')
        }
    
    def optimize_segment_boundaries(
        self,
        audio_path: str,
        segments_info: List[Dict]
    ) -> List[Dict]:
        """
        Tối ưu hóa boundaries bằng cách detect silence
        (Optional enhancement)
        """
        audio = AudioSegment.from_file(audio_path)
        
        optimized = []
        
        for segment_info in segments_info:
            start = segment_info['start']
            end = segment_info['end']
            
            # Tìm silence trước và sau
            search_window_ms = 500  # 0.5 second
            
            # Silence before
            start_ms = int(start * 1000)
            search_start = max(0, start_ms - search_window_ms)
            before_chunk = audio[search_start:start_ms]
            
            silence_before = detect_silence(
                before_chunk,
                min_silence_len=50,
                silence_thresh=self.config['alignment']['silence_threshold']
            )
            
            if silence_before:
                # Điều chỉnh start về vị trí silence cuối cùng
                last_silence = silence_before[-1]
                new_start = (search_start + last_silence[1]) / 1000
                segment_info['start'] = new_start
            
            # Tương tự cho end
            end_ms = int(end * 1000)
            search_end = min(len(audio), end_ms + search_window_ms)
            after_chunk = audio[end_ms:search_end]
            
            silence_after = detect_silence(
                after_chunk,
                min_silence_len=50,
                silence_thresh=self.config['alignment']['silence_threshold']
            )
            
            if silence_after:
                first_silence = silence_after[0]
                new_end = (end_ms + first_silence[0]) / 1000
                segment_info['end'] = new_end
            
            optimized.append(segment_info)
        
        return optimized


def test_cutter():
    """Test function"""
    config = {
        'audio_segmentation': {
            'padding_before': 0.1,
            'padding_after': 0.1,
            'min_duration': 0.5,
            'max_duration': 15.0,
            'output_sample_rate': 16000,
            'output_format': 'wav',
            'output_channels': 1
        },
        'export': {
            'naming_pattern': 'segment_{index:04d}'
        },
        'alignment': {
            'silence_threshold': -40
        }
    }
    
    cutter = AudioCutter(config)
    
    # Mock aligned sentences
    aligned_sentences = [
        {'text': 'Câu thứ nhất', 'start': 0.0, 'end': 1.5, 'confidence': 0.95},
        {'text': 'Câu thứ hai', 'start': 1.5, 'end': 3.0, 'confidence': 0.92},
    ]
    
    # Test với file audio thật (cần có file để test)
    # segments = cutter.cut_audio("sample.wav", aligned_sentences, "./output/segments")
    # for seg in segments:
    #     print(f"{seg['filename']}: {seg['text']}")
    
    print("AudioCutter module ready!")


if __name__ == "__main__":
    test_cutter()
