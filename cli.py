"""
Command Line Interface for Audio Text Segmentation Tool
"""

import os
import sys
import yaml
import argparse
from tqdm import tqdm

from core.transcriber import Transcriber
from core.sentence_splitter import SentenceSplitter
from core.aligner import Aligner
from core.audio_cutter import AudioCutter
from core.exporter import Exporter


def load_config(config_path='config.yaml'):
    """Load configuration"""
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found!")
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def process_audio(audio_path, output_dir, config):
    """Main processing pipeline"""
    
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}")
        return False
    
    audio_filename = os.path.basename(audio_path)
    print(f"\n{'='*60}")
    print(f"Processing: {audio_filename}")
    print(f"{'='*60}")
    
    try:
        # Initialize processors
        print("\n[1/5] Initializing processors...")
        transcriber = Transcriber(config)
        sentence_splitter = SentenceSplitter(config)
        aligner = Aligner(config)
        audio_cutter = AudioCutter(config)
        exporter = Exporter(config)
        
        # Step 1: Transcribe
        print("\n[2/5] Transcribing audio...")
        transcription = transcriber.transcribe(audio_path)
        print(f"  ✓ Language: {transcription['language']}")
        print(f"  ✓ Duration: {transcription.get('duration', 'N/A')}s")
        print(f"  ✓ Text length: {len(transcription['text'])} chars")
        
        # Step 2: Split sentences
        print("\n[3/5] Splitting sentences...")
        sentences = sentence_splitter.split_sentences(
            transcription['text'],
            language=transcription['language']
        )
        print(f"  ✓ Total sentences: {len(sentences)}")
        
        # Step 3: Align
        print("\n[4/5] Aligning timestamps...")
        aligned_sentences = aligner.align_sentences(sentences, transcription)
        print(f"  ✓ Aligned: {len(aligned_sentences)} sentences")
        
        # Step 4: Cut audio
        print("\n[5/5] Cutting audio segments...")
        
        # Prepare output directory
        if config['output']['create_subfolder']:
            base_name = os.path.splitext(audio_filename)[0]
            final_output_dir = os.path.join(output_dir, base_name)
        else:
            final_output_dir = output_dir
        
        os.makedirs(final_output_dir, exist_ok=True)
        
        segments_dir = os.path.join(final_output_dir, "segments")
        segments_info = audio_cutter.cut_audio(
            audio_path,
            aligned_sentences,
            segments_dir
        )
        
        # Step 5: Export
        print("\n[6/6] Exporting results...")
        exporter.export_all(
            segments_info,
            final_output_dir,
            audio_filename,
            transcription
        )
        
        print(f"\n{'='*60}")
        print("✓ PROCESSING COMPLETE!")
        print(f"  Total segments: {len(segments_info)}")
        print(f"  Output: {final_output_dir}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def batch_process(input_dir, output_dir, config):
    """Process multiple audio files"""
    
    # Find all audio files
    audio_extensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
    audio_files = []
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return
    
    print(f"\nFound {len(audio_files)} audio files")
    print(f"Output directory: {output_dir}\n")
    
    success_count = 0
    
    for i, audio_path in enumerate(audio_files, 1):
        print(f"\n{'#'*60}")
        print(f"File {i}/{len(audio_files)}")
        print(f"{'#'*60}")
        
        if process_audio(audio_path, output_dir, config):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"  Total files: {len(audio_files)}")
    print(f"  Success: {success_count}")
    print(f"  Failed: {len(audio_files) - success_count}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Audio Text Segmentation Tool - CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  python cli.py --audio input.wav --output ./results
  
  # Process with custom config
  python cli.py --audio input.wav --output ./results --config my_config.yaml
  
  # Batch process all files in a directory
  python cli.py --batch ./audio_folder --output ./results
  
  # Override language setting
  python cli.py --audio input.wav --output ./results --language en
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--audio',
        type=str,
        help='Path to audio file'
    )
    input_group.add_argument(
        '--batch',
        type=str,
        help='Path to directory containing audio files (batch processing)'
    )
    
    # Output
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output directory'
    )
    
    # Config
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to config file (default: config.yaml)'
    )
    
    # Override settings
    parser.add_argument(
        '--language',
        type=str,
        choices=['vi', 'en', 'auto'],
        help='Override language setting'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Override model size'
    )
    
    parser.add_argument(
        '--device',
        type=str,
        choices=['cpu', 'cuda'],
        help='Override device (cpu or cuda)'
    )
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Apply overrides
    if args.language:
        config['stt']['language'] = args.language
    
    if args.model:
        config['stt']['model'] = args.model
    
    if args.device:
        config['stt']['device'] = args.device
    
    # Process
    if args.audio:
        # Single file processing
        success = process_audio(args.audio, args.output, config)
        sys.exit(0 if success else 1)
    
    elif args.batch:
        # Batch processing
        batch_process(args.batch, args.output, config)
        sys.exit(0)


if __name__ == "__main__":
    main()
