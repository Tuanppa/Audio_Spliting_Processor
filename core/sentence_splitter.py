"""
Sentence Splitting Module
Tách text thành các câu độc lập với hỗ trợ tiếng Việt
"""

import re
from typing import List, Dict
import nltk

# Download NLTK data nếu chưa có
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)


class SentenceSplitter:
    """Tách text thành các câu với hỗ trợ đa ngôn ngữ"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.min_length = config['sentence_splitter']['min_length']
        self.max_length = config['sentence_splitter']['max_length']
        self.merge_short = config['sentence_splitter']['merge_short_sentences']
        self.sentence_endings = config['sentence_splitter']['sentence_endings']
        
        # Load underthesea cho tiếng Việt
        try:
            from underthesea import sent_tokenize
            self.vi_sent_tokenize = sent_tokenize
            self.has_underthesea = True
        except ImportError:
            print("Warning: underthesea not installed, using basic splitting for Vietnamese")
            self.has_underthesea = False
    
    def split_sentences(self, text: str, language: str = "vi") -> List[str]:
        """
        Tách text thành các câu
        
        Args:
            text: Text cần tách
            language: Ngôn ngữ (vi/en/auto)
            
        Returns:
            List các câu
        """
        if not text or not text.strip():
            return []
        
        # Làm sạch text
        text = self._clean_text(text)
        
        # Tách câu theo ngôn ngữ
        if language == "vi" and self.has_underthesea:
            sentences = self._split_vietnamese(text)
        elif language == "en":
            sentences = self._split_english(text)
        else:
            sentences = self._split_basic(text)
        
        # Post-processing
        sentences = self._post_process_sentences(sentences)
        
        return sentences
    
    def _clean_text(self, text: str) -> str:
        """Làm sạch text"""
        # Loại bỏ khoảng trắng thừa
        text = re.sub(r'\s+', ' ', text)
        
        # Loại bỏ ký tự đặc biệt không cần thiết (giữ lại dấu câu)
        text = re.sub(r'[^\w\s\.,;:!?\'\"()áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ-]', '', text)
        
        return text.strip()
    
    def _split_vietnamese(self, text: str) -> List[str]:
        """Tách câu tiếng Việt sử dụng underthesea"""
        try:
            sentences = self.vi_sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            print(f"Error in Vietnamese tokenization: {e}")
            return self._split_basic(text)
    
    def _split_english(self, text: str) -> List[str]:
        """Tách câu tiếng Anh sử dụng NLTK"""
        try:
            sentences = nltk.sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except Exception as e:
            print(f"Error in English tokenization: {e}")
            return self._split_basic(text)
    
    def _split_basic(self, text: str) -> List[str]:
        """Tách câu cơ bản dựa trên dấu câu"""
        # Tạo pattern từ danh sách dấu kết thúc câu
        endings_pattern = '|'.join(re.escape(end) for end in self.sentence_endings)
        
        # Tách dựa trên dấu kết thúc câu
        pattern = f'([^{endings_pattern}]+[{endings_pattern}]+)'
        sentences = re.findall(pattern, text)
        
        # Nếu không tìm thấy dấu kết thúc, trả về toàn bộ text
        if not sentences:
            return [text.strip()] if text.strip() else []
        
        return [s.strip() for s in sentences if s.strip()]
    
    def _post_process_sentences(self, sentences: List[str]) -> List[str]:
        """Post-process các câu sau khi tách"""
        if not sentences:
            return []
        
        processed = []
        
        for sentence in sentences:
            # Bỏ qua câu quá ngắn hoặc quá dài
            if len(sentence) < self.min_length:
                if self.merge_short and processed:
                    # Gộp với câu trước
                    processed[-1] = processed[-1] + " " + sentence
                else:
                    processed.append(sentence)
                continue
            
            if len(sentence) > self.max_length:
                # Chia câu dài thành nhiều câu nhỏ hơn
                sub_sentences = self._split_long_sentence(sentence)
                processed.extend(sub_sentences)
            else:
                processed.append(sentence)
        
        return processed
    
    def _split_long_sentence(self, sentence: str) -> List[str]:
        """Chia câu quá dài thành nhiều câu nhỏ hơn"""
        # Thử tách theo dấu phẩy, chấm phẩy
        parts = re.split(r'[,;]', sentence)
        
        result = []
        current = ""
        
        for part in parts:
            part = part.strip()
            if len(current) + len(part) <= self.max_length:
                current = current + " " + part if current else part
            else:
                if current:
                    result.append(current.strip())
                current = part
        
        if current:
            result.append(current.strip())
        
        # Nếu vẫn có câu dài, chia theo số ký tự
        final_result = []
        for part in result:
            if len(part) > self.max_length:
                # Chia theo khoảng trắng gần nhất
                words = part.split()
                temp = ""
                for word in words:
                    if len(temp) + len(word) + 1 <= self.max_length:
                        temp = temp + " " + word if temp else word
                    else:
                        if temp:
                            final_result.append(temp.strip())
                        temp = word
                if temp:
                    final_result.append(temp.strip())
            else:
                final_result.append(part)
        
        return final_result


def test_splitter():
    """Test function"""
    config = {
        'sentence_splitter': {
            'min_length': 10,
            'max_length': 200,
            'merge_short_sentences': True,
            'sentence_endings': ['.', '?', '!']
        }
    }
    
    splitter = SentenceSplitter(config)
    
    # Test tiếng Việt
    text_vi = "Xin chào các bạn. Đây là một bài test. Mục đích để kiểm tra việc tách câu!"
    sentences = splitter.split_sentences(text_vi, language="vi")
    print("Vietnamese sentences:")
    for i, sent in enumerate(sentences, 1):
        print(f"{i}. {sent}")
    
    # Test tiếng Anh
    text_en = "Hello everyone. This is a test. The purpose is to check sentence splitting!"
    sentences = splitter.split_sentences(text_en, language="en")
    print("\nEnglish sentences:")
    for i, sent in enumerate(sentences, 1):
        print(f"{i}. {sent}")


if __name__ == "__main__":
    test_splitter()
