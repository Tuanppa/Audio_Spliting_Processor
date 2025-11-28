"""
Export Module
Xuất kết quả processing ra các định dạng: JSON, CSV, text files
"""

import os
import json
import csv
from typing import List, Dict
from datetime import datetime


class Exporter:
    """Xuất kết quả processing"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.create_manifest = config['export']['create_manifest']
        self.create_csv = config['export']['create_csv']
        self.create_full_transcript = config['export']['create_full_transcript']
        self.include_confidence = config['export']['include_confidence']
    
    def export_all(
        self,
        segments_info: List[Dict],
        output_dir: str,
        audio_filename: str,
        transcription: Dict
    ):
        """
        Xuất tất cả các định dạng output
        
        Args:
            segments_info: List các segment đã cắt
            output_dir: Thư mục output
            audio_filename: Tên file audio gốc
            transcription: Kết quả transcription đầy đủ
        """
        print("\nExporting results...")
        
        # Tạo thư mục segments nếu chưa có
        segments_dir = os.path.join(output_dir, "segments")
        os.makedirs(segments_dir, exist_ok=True)
        
        # Export individual text files cho mỗi segment
        self._export_segment_texts(segments_info, segments_dir)
        
        # Export manifest.json
        if self.create_manifest:
            self._export_manifest(
                segments_info,
                output_dir,
                audio_filename,
                transcription
            )
        
        # Export metadata.csv
        if self.create_csv:
            self._export_csv(segments_info, output_dir)
        
        # Export full transcript
        if self.create_full_transcript:
            self._export_full_transcript(transcription, output_dir)
        
        print(f"✓ All results exported to: {output_dir}")
    
    def _export_segment_texts(self, segments_info: List[Dict], output_dir: str):
        """Xuất file text cho mỗi segment"""
        for segment in segments_info:
            # Generate text filename (same base name as audio)
            audio_filename = segment['filename']
            base_name = os.path.splitext(audio_filename)[0]
            text_filename = f"{base_name}.txt"
            text_path = os.path.join(output_dir, text_filename)
            
            # Write text
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(segment['text'])
        
        print(f"✓ Exported {len(segments_info)} text files")
    
    def _export_manifest(
        self,
        segments_info: List[Dict],
        output_dir: str,
        audio_filename: str,
        transcription: Dict
    ):
        """Xuất manifest.json với metadata đầy đủ"""
        
        manifest = {
            'metadata': {
                'original_audio': audio_filename,
                'processing_date': datetime.now().isoformat(),
                'language': transcription.get('language', 'unknown'),
                'total_duration': transcription.get('duration'),
                'total_segments': len(segments_info),
                'config': self.config
            },
            'segments': []
        }
        
        for segment in segments_info:
            segment_data = {
                'index': segment['index'],
                'filename': segment['filename'],
                'text': segment['text'],
                'start': round(segment['start'], 3),
                'end': round(segment['end'], 3),
                'duration': round(segment['duration'], 3),
                'audio_info': {
                    'sample_rate': segment['sample_rate'],
                    'channels': segment['channels']
                }
            }
            
            if self.include_confidence and segment.get('confidence') is not None:
                segment_data['confidence'] = round(segment['confidence'], 3)
            
            manifest['segments'].append(segment_data)
        
        manifest_path = os.path.join(output_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Exported manifest.json")
    
    def _export_csv(self, segments_info: List[Dict], output_dir: str):
        """Xuất metadata.csv"""
        
        csv_path = os.path.join(output_dir, 'metadata.csv')
        
        # Determine fields
        fieldnames = [
            'index',
            'filename',
            'text',
            'start',
            'end',
            'duration',
            'sample_rate',
            'channels'
        ]
        
        if self.include_confidence:
            fieldnames.append('confidence')
        
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for segment in segments_info:
                row = {
                    'index': segment['index'],
                    'filename': segment['filename'],
                    'text': segment['text'],
                    'start': round(segment['start'], 3),
                    'end': round(segment['end'], 3),
                    'duration': round(segment['duration'], 3),
                    'sample_rate': segment['sample_rate'],
                    'channels': segment['channels']
                }
                
                if self.include_confidence:
                    row['confidence'] = round(segment.get('confidence', 0), 3) if segment.get('confidence') else ''
                
                writer.writerow(row)
        
        print(f"✓ Exported metadata.csv")
    
    def _export_full_transcript(self, transcription: Dict, output_dir: str):
        """Xuất full transcript text"""
        
        transcript_path = os.path.join(output_dir, 'full_transcript.txt')
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcription['text'])
        
        print(f"✓ Exported full_transcript.txt")
    
    def create_ljspeech_format(
        self,
        segments_info: List[Dict],
        output_dir: str
    ):
        """
        Tạo metadata theo format LJSpeech (phổ biến cho TTS training)
        Format: filename|text
        """
        metadata_path = os.path.join(output_dir, 'metadata_ljspeech.txt')
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            for segment in segments_info:
                # Remove extension from filename
                base_name = os.path.splitext(segment['filename'])[0]
                # Clean text (remove special chars nếu cần)
                text = segment['text'].strip()
                f.write(f"{base_name}|{text}\n")
        
        print(f"✓ Exported metadata_ljspeech.txt")
    
    def create_kaldi_format(
        self,
        segments_info: List[Dict],
        output_dir: str
    ):
        """
        Tạo format Kaldi (cho ASR training)
        Bao gồm: segments, text, utt2spk files
        """
        # segments file: utt_id audio_id start_time end_time
        segments_path = os.path.join(output_dir, 'segments')
        with open(segments_path, 'w', encoding='utf-8') as f:
            for segment in segments_info:
                utt_id = os.path.splitext(segment['filename'])[0]
                audio_id = "audio_001"  # Placeholder
                f.write(f"{utt_id} {audio_id} {segment['start']:.2f} {segment['end']:.2f}\n")
        
        # text file: utt_id transcript
        text_path = os.path.join(output_dir, 'text')
        with open(text_path, 'w', encoding='utf-8') as f:
            for segment in segments_info:
                utt_id = os.path.splitext(segment['filename'])[0]
                f.write(f"{utt_id} {segment['text']}\n")
        
        print(f"✓ Exported Kaldi format files")


def test_exporter():
    """Test function"""
    config = {
        'export': {
            'create_manifest': True,
            'create_csv': True,
            'create_full_transcript': True,
            'include_confidence': True,
            'naming_pattern': 'segment_{index:04d}'
        }
    }
    
    exporter = Exporter(config)
    
    # Mock data
    segments_info = [
        {
            'index': 0,
            'filename': 'segment_0001.wav',
            'path': './output/segments/segment_0001.wav',
            'text': 'Xin chào các bạn.',
            'start': 0.0,
            'end': 1.5,
            'duration': 1.5,
            'sample_rate': 16000,
            'channels': 1,
            'confidence': 0.95
        },
        {
            'index': 1,
            'filename': 'segment_0002.wav',
            'path': './output/segments/segment_0002.wav',
            'text': 'Đây là một bài test.',
            'start': 1.5,
            'end': 3.0,
            'duration': 1.5,
            'sample_rate': 16000,
            'channels': 1,
            'confidence': 0.92
        }
    ]
    
    transcription = {
        'text': 'Xin chào các bạn. Đây là một bài test.',
        'language': 'vi',
        'duration': 3.0
    }
    
    output_dir = './test_output'
    os.makedirs(output_dir, exist_ok=True)
    
    exporter.export_all(segments_info, output_dir, 'test.wav', transcription)
    print("Exporter module ready!")


if __name__ == "__main__":
    test_exporter()
