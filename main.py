"""
Main Entry Point - Command Line Interface cho Audio Processor
"""

import argparse
import logging
import sys
from pathlib import Path

from config import AppConfig, WhisperConfig, AudioConfig, ProcessConfig, PathConfig
from processor import AudioProcessor


def setup_logging(verbose: bool = False, log_file: str = None):
    """
    Setup logging configuration
    
    Args:
        verbose: Nếu True, hiển thị DEBUG logs
        log_file: Đường dẫn file log (optional)
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    handlers = [console_handler]
    
    # File handler (nếu có)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    logging.basicConfig(
        level=level,
        handlers=handlers
    )


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Audio Processor - Convert audio to text with segmentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  python main.py --input sample.wav --output ./output
  
  # Process batch
  python main.py --batch --input-dir ./audio_files --output-dir ./results
  
  # Use large model with GPU
  python main.py --input sample.wav --model large --device cuda
  
  # Custom segment duration
  python main.py --input sample.wav --min-duration 1.0 --max-duration 20.0
        """
    )
    
    # Input/Output
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Input audio file path (for single file processing)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory'
    )
    
    # Batch processing
    parser.add_argument(
        '--batch', '-b',
        action='store_true',
        help='Batch processing mode'
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        default='./input',
        help='Input directory for batch processing (default: ./input)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Output directory for batch processing (default: ./output)'
    )
    
    # Whisper configuration
    parser.add_argument(
        '--model', '-m',
        type=str,
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base',
        help='Whisper model size (default: base)'
    )
    parser.add_argument(
        '--device',
        type=str,
        choices=['cpu', 'cuda'],
        default='cpu',
        help='Device to run model on (default: cpu)'
    )
    parser.add_argument(
        '--language',
        type=str,
        default='en',
        help='Language code (default: en)'
    )
    
    # Audio configuration
    parser.add_argument(
        '--min-duration',
        type=float,
        default=0.5,
        help='Minimum segment duration in seconds (default: 0.5)'
    )
    parser.add_argument(
        '--max-duration',
        type=float,
        default=30.0,
        help='Maximum segment duration in seconds (default: 30.0)'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='wav',
        help='Output audio format (default: wav)'
    )
    
    # Processing configuration
    parser.add_argument(
        '--prefix',
        type=str,
        default='segment',
        help='Prefix for output files (default: segment)'
    )
    
    # Logging
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Log file path'
    )
    
    # Statistics
    parser.add_argument(
        '--stats',
        type=str,
        help='Show statistics for a processed output directory'
    )
    
    return parser.parse_args()


def main():
    """
    Main function
    """
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose, args.log_file)
    logger = logging.getLogger(__name__)
    
    # Show statistics mode
    if args.stats:
        logger.info(f"Loading statistics from: {args.stats}")
        
        config = AppConfig()
        processor = AudioProcessor(config)
        stats = processor.get_processing_stats(args.stats)
        
        if "error" in stats:
            logger.error(f"Error: {stats['error']}")
            sys.exit(1)
        
        # Display stats
        print("\n" + "="*60)
        print("PROCESSING STATISTICS")
        print("="*60)
        print(f"Total Segments: {stats['total_segments']}")
        print(f"Total Duration: {stats['total_duration']:.2f}s ({stats['total_duration']/60:.2f} minutes)")
        print(f"Average Segment: {stats['avg_segment_duration']:.2f}s")
        print(f"Shortest Segment: {stats['shortest_segment']:.2f}s")
        print(f"Longest Segment: {stats['longest_segment']:.2f}s")
        print(f"Total Words: {stats['total_words']}")
        print(f"Avg Words/Segment: {stats['avg_words_per_segment']:.1f}")
        print("="*60 + "\n")
        
        return
    
    # Build configuration from arguments
    config = AppConfig(
        whisper=WhisperConfig(
            model_size=args.model,
            device=args.device,
            language=args.language
        ),
        audio=AudioConfig(
            min_segment_duration=args.min_duration,
            max_segment_duration=args.max_duration,
            format=args.format
        ),
        process=ProcessConfig(
            prefix=args.prefix
        ),
        paths=PathConfig(
            input_dir=Path(args.input_dir),
            output_dir=Path(args.output_dir)
        ),
        verbose=args.verbose
    )
    
    # Create processor
    logger.info("Initializing Audio Processor...")
    processor = AudioProcessor(config)
    
    try:
        if args.batch:
            # Batch processing
            logger.info(f"Starting batch processing from: {args.input_dir}")
            results = processor.process_batch(
                input_dir=args.input_dir,
                output_dir=args.output_dir
            )
            
            if results:
                logger.info("Batch processing completed successfully")
            else:
                logger.warning("No files were processed")
        
        elif args.input:
            # Single file processing
            logger.info(f"Processing single file: {args.input}")
            
            if not Path(args.input).exists():
                logger.error(f"Input file not found: {args.input}")
                sys.exit(1)
            
            result = processor.process_single_file(
                audio_path=args.input,
                output_dir=args.output
            )
            
            if result["status"] == "success":
                logger.info("Processing completed successfully")
                
                # Show quick stats
                print("\n" + "="*60)
                print(f"✓ Processed: {result['total_segments']} segments")
                print(f"✓ Duration: {result['total_duration']:.2f}s")
                print(f"✓ Output: {result['output_dir']}")
                print("="*60 + "\n")
            else:
                logger.error(f"Processing failed: {result.get('reason', 'Unknown error')}")
                sys.exit(1)
        
        else:
            logger.error("No input specified. Use --input or --batch mode")
            logger.info("Run with --help for usage information")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.warning("\nProcessing interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error during processing: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
