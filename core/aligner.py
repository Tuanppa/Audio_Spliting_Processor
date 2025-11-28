"""
Text-Audio Alignment Module
Căn chỉnh timestamps chính xác giữa các câu text và audio segments
"""

import re
from typing import List, Dict, Tuple, Optional
import numpy as np


class Aligner:
    """Căn chỉnh timestamps giữa sentences và audio segments"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.method = config['alignment']['method']
        self.optimize_boundaries = config['alignment'].get('optimize_boundaries', True)
        self.silence_threshold = config['alignment'].get('silence_threshold', -40)
    
    def align_sentences(
        self,
        sentences: List[str],
        transcription: Dict
    ) -> List[Dict]:
        """
        Căn chỉnh sentences với timestamps từ transcription
        
        Args:
            sentences: List các câu đã tách
            transcription: Kết quả transcription từ Transcriber
            
        Returns:
            List of {text, start, end, confidence}
        """
        if self.method == "whisper":
            return self._align_with_whisper_timestamps(sentences, transcription)
        else:
            # Có thể implement aeneas hoặc methods khác
            return self._align_with_whisper_timestamps(sentences, transcription)
    
    def _align_with_whisper_timestamps(
        self,
        sentences: List[str],
        transcription: Dict
    ) -> List[Dict]:
        """Căn chỉnh sử dụng timestamps từ Whisper"""
        
        # Lấy tất cả segments và words từ transcription
        segments = transcription['segments']
        
        # Build word-level mappings nếu có
        words_timeline = self._build_words_timeline(segments)
        
        # Align từng câu
        aligned_sentences = []
        sentence_index = 0
        
        for sentence in sentences:
            sentence_clean = self._normalize_text(sentence)
            
            # Tìm vị trí câu này trong timeline
            alignment = self._find_sentence_in_timeline(
                sentence_clean,
                words_timeline,
                sentence_index
            )
            
            if alignment:
                aligned_sentences.append({
                    'text': sentence,
                    'start': alignment['start'],
                    'end': alignment['end'],
                    'confidence': alignment.get('confidence', None)
                })
                sentence_index = alignment.get('next_index', sentence_index + 1)
            else:
                # Không tìm được alignment, sử dụng estimate
                print(f"Warning: Could not align sentence: {sentence[:50]}...")
                if aligned_sentences:
                    # Estimate dựa trên câu trước
                    prev = aligned_sentences[-1]
                    estimated_start = prev['end']
                    estimated_duration = len(sentence) * 0.05  # Rough estimate
                    aligned_sentences.append({
                        'text': sentence,
                        'start': estimated_start,
                        'end': estimated_start + estimated_duration,
                        'confidence': None
                    })
                else:
                    # Câu đầu tiên, bắt đầu từ 0
                    estimated_duration = len(sentence) * 0.05
                    aligned_sentences.append({
                        'text': sentence,
                        'start': 0.0,
                        'end': estimated_duration,
                        'confidence': None
                    })
        
        # Optimize boundaries nếu cần
        if self.optimize_boundaries:
            aligned_sentences = self._optimize_boundaries(aligned_sentences)
        
        return aligned_sentences
    
    def _build_words_timeline(self, segments: List[Dict]) -> List[Dict]:
        """Xây dựng timeline của tất cả các từ"""
        words_timeline = []
        
        for segment in segments:
            # Nếu có word-level timestamps
            if 'words' in segment:
                for word_info in segment['words']:
                    words_timeline.append({
                        'word': self._normalize_text(word_info['word']),
                        'start': word_info['start'],
                        'end': word_info['end']
                    })
            else:
                # Fallback: sử dụng segment-level timestamps
                # Chia đều thời gian cho các từ trong segment
                text = segment['text'].strip()
                words = text.split()
                segment_duration = segment['end'] - segment['start']
                word_duration = segment_duration / len(words) if words else 0
                
                for i, word in enumerate(words):
                    words_timeline.append({
                        'word': self._normalize_text(word),
                        'start': segment['start'] + i * word_duration,
                        'end': segment['start'] + (i + 1) * word_duration
                    })
        
        return words_timeline
    
    def _find_sentence_in_timeline(
        self,
        sentence: str,
        words_timeline: List[Dict],
        start_index: int = 0
    ) -> Optional[Dict]:
        """Tìm vị trí câu trong timeline"""
        
        sentence_words = sentence.split()
        if not sentence_words:
            return None
        
        # Tìm first word của câu
        first_word = self._normalize_text(sentence_words[0])
        last_word = self._normalize_text(sentence_words[-1])
        
        # Tìm matching sequence
        best_match = None
        max_match_ratio = 0.5  # Threshold
        
        for i in range(start_index, len(words_timeline)):
            # Thử match từ vị trí i
            match_count = 0
            j = 0
            
            for word in sentence_words:
                word_norm = self._normalize_text(word)
                # Tìm word trong timeline từ vị trí i+j
                if i + j < len(words_timeline):
                    timeline_word = words_timeline[i + j]['word']
                    if self._words_match(word_norm, timeline_word):
                        match_count += 1
                        j += 1
                    else:
                        # Cho phép skip 1 từ
                        if i + j + 1 < len(words_timeline):
                            timeline_word_next = words_timeline[i + j + 1]['word']
                            if self._words_match(word_norm, timeline_word_next):
                                match_count += 1
                                j += 2
                            else:
                                break
                        else:
                            break
                else:
                    break
            
            # Tính match ratio
            match_ratio = match_count / len(sentence_words)
            
            if match_ratio > max_match_ratio:
                max_match_ratio = match_ratio
                # Lấy start từ từ đầu tiên, end từ từ cuối cùng
                if i < len(words_timeline) and i + j - 1 < len(words_timeline):
                    best_match = {
                        'start': words_timeline[i]['start'],
                        'end': words_timeline[min(i + j - 1, len(words_timeline) - 1)]['end'],
                        'confidence': match_ratio,
                        'next_index': i + j
                    }
            
            # Nếu đã match tốt, dừng
            if match_ratio > 0.9:
                break
        
        return best_match
    
    def _normalize_text(self, text: str) -> str:
        """Chuẩn hóa text để so sánh"""
        # Lowercase
        text = text.lower()
        # Loại bỏ dấu câu
        text = re.sub(r'[^\w\s]', '', text)
        # Loại bỏ khoảng trắng thừa
        text = ' '.join(text.split())
        return text
    
    def _words_match(self, word1: str, word2: str, threshold: float = 0.8) -> bool:
        """Kiểm tra 2 từ có match không"""
        # Exact match
        if word1 == word2:
            return True
        
        # Partial match (cho phép sai khác nhỏ)
        if len(word1) < 3 or len(word2) < 3:
            return False
        
        # Levenshtein distance (simplified)
        max_len = max(len(word1), len(word2))
        matching_chars = sum(c1 == c2 for c1, c2 in zip(word1, word2))
        similarity = matching_chars / max_len
        
        return similarity >= threshold
    
    def _optimize_boundaries(self, aligned_sentences: List[Dict]) -> List[Dict]:
        """Tối ưu hóa boundaries giữa các câu"""
        
        if len(aligned_sentences) <= 1:
            return aligned_sentences
        
        optimized = []
        
        for i, sentence in enumerate(aligned_sentences):
            if i == 0:
                # Câu đầu tiên
                optimized.append(sentence.copy())
            else:
                # Kiểm tra gap với câu trước
                prev_sentence = optimized[-1]
                gap = sentence['start'] - prev_sentence['end']
                
                if gap < 0:
                    # Overlap: chia đều
                    midpoint = (prev_sentence['end'] + sentence['start']) / 2
                    optimized[-1]['end'] = midpoint
                    sentence = sentence.copy()
                    sentence['start'] = midpoint
                elif gap > 1.0:
                    # Gap lớn: extend prev sentence
                    optimized[-1]['end'] = sentence['start'] - 0.1
                
                optimized.append(sentence)
        
        return optimized


def test_aligner():
    """Test function"""
    config = {
        'alignment': {
            'method': 'whisper',
            'optimize_boundaries': True,
            'silence_threshold': -40
        }
    }
    
    aligner = Aligner(config)
    
    # Mock data
    sentences = [
        "Xin chào các bạn.",
        "Đây là một bài test.",
        "Mục đích để kiểm tra alignment."
    ]
    
    transcription = {
        'segments': [
            {
                'text': 'Xin chào các bạn.',
                'start': 0.0,
                'end': 1.5,
                'words': [
                    {'word': 'Xin', 'start': 0.0, 'end': 0.3},
                    {'word': 'chào', 'start': 0.3, 'end': 0.7},
                    {'word': 'các', 'start': 0.7, 'end': 1.0},
                    {'word': 'bạn', 'start': 1.0, 'end': 1.5}
                ]
            },
            {
                'text': 'Đây là một bài test.',
                'start': 1.5,
                'end': 3.2,
            }
        ]
    }
    
    result = aligner.align_sentences(sentences, transcription)
    print("Aligned sentences:")
    for item in result:
        print(f"[{item['start']:.2f}-{item['end']:.2f}] {item['text']}")


if __name__ == "__main__":
    test_aligner()
