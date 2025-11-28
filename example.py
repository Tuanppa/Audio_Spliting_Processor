"""
Example script - Demonstrates how to use Audio Processor in Python code
"""

import logging
from pathlib import Path
from config import AppConfig, WhisperConfig, AudioConfig
from processor import AudioProcessor


def example_single_file():
    """
    Example 1: Xử lý một file audio đơn lẻ
    """
    print("\n" + "="*60)
    print("Example 1: Processing single audio file")
    print("="*60 + "\n")
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Tạo config
    config = AppConfig(
        whisper=WhisperConfig(
            model_size="base",  # tiny, base, small, medium, large
            device="cpu"        # cpu hoặc cuda
        ),
        audio=AudioConfig(
            min_segment_duration=0.5,
            max_segment_duration=30.0
        )
    )
    
    # Khởi tạo processor
    processor = AudioProcessor(config)
    
    # Xử lý file
    # NOTE: Thay "sample.wav" bằng đường dẫn file audio thực tế của bạn
    audio_path = "sample.wav"
    
    if Path(audio_path).exists():
        result = processor.process_single_file(
            audio_path=audio_path,
            output_dir="./output/example1"
        )
        
        print("\nResult:", result)
    else:
        print(f"⚠ File not found: {audio_path}")
        print("Please place an audio file named 'sample.wav' in the current directory")


def example_batch_processing():
    """
    Example 2: Xử lý batch nhiều file
    """
    print("\n" + "="*60)
    print("Example 2: Batch processing multiple files")
    print("="*60 + "\n")
    
    logging.basicConfig(level=logging.INFO)
    
    config = AppConfig()
    processor = AudioProcessor(config)
    
    # Xử lý tất cả files trong thư mục input/
    # NOTE: Đặt audio files vào thư mục "input/" trước khi chạy
    if Path("./input").exists():
        results = processor.process_batch(
            input_dir="./input",
            output_dir="./output/batch"
        )
        
        print(f"\n✓ Processed {len(results)} files")
    else:
        print("⚠ Directory './input' not found")
        print("Please create './input' directory and add audio files")


def example_custom_config():
    """
    Example 3: Sử dụng custom configuration
    """
    print("\n" + "="*60)
    print("Example 3: Using custom configuration")
    print("="*60 + "\n")
    
    logging.basicConfig(level=logging.INFO)
    
    # Custom config cho segments ngắn (good for TTS training)
    config = AppConfig(
        whisper=WhisperConfig(
            model_size="small",  # Model chính xác hơn
            device="cpu"
        ),
        audio=AudioConfig(
            min_segment_duration=1.0,   # Tối thiểu 1 giây
            max_segment_duration=10.0,  # Tối đa 10 giây
            format="wav",
            sample_rate=22050  # Higher quality cho TTS
        )
    )
    
    processor = AudioProcessor(config)
    
    # Process
    audio_path = "sample.wav"
    if Path(audio_path).exists():
        result = processor.process_single_file(
            audio_path=audio_path,
            output_dir="./output/custom_config"
        )
        print("\nCustom config result:", result)
    else:
        print(f"⚠ File not found: {audio_path}")


def example_statistics():
    """
    Example 4: Xem thống kê của output đã xử lý
    """
    print("\n" + "="*60)
    print("Example 4: Getting processing statistics")
    print("="*60 + "\n")
    
    logging.basicConfig(level=logging.INFO)
    
    config = AppConfig()
    processor = AudioProcessor(config)
    
    # Lấy stats từ một output directory
    output_dir = "./output/example1"  # Thay bằng path thực tế
    
    if Path(output_dir).exists():
        stats = processor.get_processing_stats(output_dir)
        
        print("\nStatistics:")
        print(f"  Total Segments: {stats.get('total_segments', 'N/A')}")
        print(f"  Total Duration: {stats.get('total_duration', 'N/A'):.2f}s")
        print(f"  Average Duration: {stats.get('avg_segment_duration', 'N/A'):.2f}s")
        print(f"  Total Words: {stats.get('total_words', 'N/A')}")
    else:
        print(f"⚠ Directory not found: {output_dir}")
        print("Please run example_single_file() first")


def example_transcription_only():
    """
    Example 5: Chỉ transcribe, không cắt audio
    """
    print("\n" + "="*60)
    print("Example 5: Transcription only (no audio segmentation)")
    print("="*60 + "\n")
    
    logging.basicConfig(level=logging.INFO)
    
    from transcriber import AudioTranscriber
    
    config = WhisperConfig(model_size="base", device="cpu")
    transcriber = AudioTranscriber(config)
    
    audio_path = "sample.wav"
    
    if Path(audio_path).exists():
        # Transcribe
        segments = transcriber.transcribe_to_sentences(audio_path)
        
        # Save transcript
        transcriber.save_transcript(segments, "transcript.txt")
        transcriber.save_transcript_json(segments, "transcript.json")
        
        print(f"\n✓ Transcribed {len(segments)} segments")
        print("✓ Saved to transcript.txt and transcript.json")
        
        # Show first few segments
        print("\nFirst 3 segments:")
        for seg in segments[:3]:
            print(f"  [{seg.start:.2f}s - {seg.end:.2f}s] {seg.text}")
    else:
        print(f"⚠ File not found: {audio_path}")


def main():
    """
    Main function - chạy tất cả examples
    """
    print("""
╔══════════════════════════════════════════════════════════╗
║         Audio Processor - Example Usage                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    print("Available examples:")
    print("  1. Single file processing")
    print("  2. Batch processing")
    print("  3. Custom configuration")
    print("  4. View statistics")
    print("  5. Transcription only")
    print("")
    
    choice = input("Select example (1-5) or 'all' to run all: ").strip()
    
    if choice == "1":
        example_single_file()
    elif choice == "2":
        example_batch_processing()
    elif choice == "3":
        example_custom_config()
    elif choice == "4":
        example_statistics()
    elif choice == "5":
        example_transcription_only()
    elif choice.lower() == "all":
        example_single_file()
        example_batch_processing()
        example_custom_config()
        example_statistics()
        example_transcription_only()
    else:
        print("Invalid choice. Please run again.")


if __name__ == "__main__":
    main()
