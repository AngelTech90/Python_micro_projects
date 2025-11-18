#!/usr/bin/env python3
"""
Video/Audio Separator
Extract video (no audio) and audio tracks into separate directories using FFmpeg
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict
import argparse
import json


class MediaSeparator:
    """Separate video and audio tracks using FFmpeg"""
    
    def __init__(self, video_dir: str = "videos", audio_dir: str = "audio"):
        """
        Initialize separator with output directories
        
        Args:
            video_dir: Directory for video-only files
            audio_dir: Directory for audio-only files
        """
        self.video_dir = Path(video_dir)
        self.audio_dir = Path(audio_dir)
        
        # Create output directories
        self.video_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Video output: {self.video_dir}/")
        print(f"Audio output: {self.audio_dir}/")
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg not found. Install it:\n"
                "  Ubuntu/Debian: sudo apt install ffmpeg\n"
                "  Fedora: sudo dnf install ffmpeg\n"
                "  macOS: brew install ffmpeg"
            )
    
    def get_media_info(self, file_path: str) -> Dict:
        """Get media file information using ffprobe"""
        try:
            result = subprocess.run([
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-show_format',
                file_path
            ], capture_output=True, text=True, check=True)
            
            data = json.loads(result.stdout)
            
            # Identify streams
            has_video = any(s['codec_type'] == 'video' for s in data['streams'])
            has_audio = any(s['codec_type'] == 'audio' for s in data['streams'])
            
            return {
                'has_video': has_video,
                'has_audio': has_audio,
                'streams': data['streams'],
                'format': data['format']
            }
        except Exception as e:
            raise Exception(f"Failed to analyze {file_path}: {str(e)}")
    
    def extract_video(self, input_file: str, output_file: str):
        """
        Extract video stream without audio
        
        Args:
            input_file: Source video file
            output_file: Output video file (no audio)
        """
        print(f"  Extracting video: {Path(input_file).name}")
        
        subprocess.run([
            'ffmpeg',
            '-i', input_file,
            '-an',                    # No audio
            '-c:v', 'copy',           # Copy video codec (no re-encoding)
            '-y',                     # Overwrite output
            output_file
        ], capture_output=True, check=True)
        
        print(f"    ✓ Video saved: {output_file}")
    
    def extract_audio(self, input_file: str, output_file: str, format: str = 'mp3'):
        """
        Extract audio stream
        
        Args:
            input_file: Source video file
            output_file: Output audio file
            format: Output format ('mp3', 'wav', 'aac', 'm4a', 'flac')
        """
        print(f"  Extracting audio: {Path(input_file).name}")
        
        # Codec settings for different formats
        codecs = {
            'mp3': ['libmp3lame', '-q:a', '0'],      # High quality MP3
            'wav': ['pcm_s16le'],                    # 16-bit WAV
            'aac': ['aac', '-b:a', '320k'],          # High quality AAC
            'm4a': ['aac', '-b:a', '320k'],          # M4A container
            'flac': ['flac'],                        # Lossless FLAC
            'ogg': ['libvorbis', '-q:a', '10']       # High quality OGG
        }
        
        if format not in codecs:
            raise ValueError(f"Unsupported format: {format}")
        
        codec_args = codecs[format]
        
        subprocess.run([
            'ffmpeg',
            '-i', input_file,
            '-vn',                    # No video
            '-acodec', codec_args[0],
            *codec_args[1:],
            '-y',
            output_file
        ], capture_output=True, check=True)
        
        print(f"    ✓ Audio saved: {output_file}")
    
    def separate_file(
        self,
        input_file: str,
        video_format: str = 'mp4',
        audio_format: str = 'mp3'
    ) -> Dict:
        """
        Separate single file into video and audio
        
        Args:
            input_file: Input video file
            video_format: Output video format (default: mp4)
            audio_format: Output audio format (default: mp3)
            
        Returns:
            Dictionary with paths to extracted files
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_file}")
        
        print(f"\n{'='*60}")
        print(f"Processing: {input_path.name}")
        print('='*60)
        
        # Check media streams
        info = self.get_media_info(str(input_path))
        
        if not info['has_video'] and not info['has_audio']:
            raise Exception("File has no video or audio streams")
        
        result = {'input': str(input_path)}
        
        try:
            # Extract video (if present)
            if info['has_video']:
                video_output = self.video_dir / f"{input_path.stem}.{video_format}"
                self.extract_video(str(input_path), str(video_output))
                result['video'] = str(video_output)
            else:
                print("  ⚠ No video stream found")
                result['video'] = None
            
            # Extract audio (if present)
            if info['has_audio']:
                audio_output = self.audio_dir / f"{input_path.stem}.{audio_format}"
                self.extract_audio(str(input_path), str(audio_output), audio_format)
                result['audio'] = str(audio_output)
            else:
                print("  ⚠ No audio stream found")
                result['audio'] = None
            
            print(f"✓ Complete!\n")
            result['status'] = 'success'
            return result
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}\n")
            result['status'] = 'failed'
            result['error'] = str(e)
            return result
    
    def separate_batch(
        self,
        input_files: List[str],
        video_format: str = 'mp4',
        audio_format: str = 'mp3'
    ) -> Dict:
        """
        Separate multiple files
        
        Args:
            input_files: List of input video files
            video_format: Output video format
            audio_format: Output audio format
            
        Returns:
            Summary dictionary
        """
        print(f"\n{'='*60}")
        print(f"BATCH SEPARATION: {len(input_files)} files")
        print(f"Video directory: {self.video_dir}/")
        print(f"Audio directory: {self.audio_dir}/")
        print('='*60)
        
        results = {
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for i, input_file in enumerate(input_files, 1):
            print(f"\n[{i}/{len(input_files)}]")
            
            result = self.separate_file(input_file, video_format, audio_format)
            results['files'].append(result)
            
            if result['status'] == 'success':
                results['success'] += 1
            else:
                results['failed'] += 1
        
        # Summary
        print("\n" + "="*60)
        print("BATCH SEPARATION COMPLETE")
        print("="*60)
        print(f"Total files: {len(input_files)}")
        print(f"Success: {results['success']}")
        print(f"Failed: {results['failed']}")
        print(f"\nOutput locations:")
        print(f"  Videos: {self.video_dir}/")
        print(f"  Audio: {self.audio_dir}/")
        print("="*60 + "\n")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Separate video and audio tracks using FFmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file (default: MP4 video + MP3 audio)
  python separator.py input.mp4
  
  # Multiple files
  python separator.py video1.mp4 video2.mkv video3.avi
  
  # Custom output directories
  python separator.py input.mp4 --video-dir my_videos --audio-dir my_audio
  
  # Custom output formats
  python separator.py input.mp4 --video-format mkv --audio-format wav
  
  # Batch process directory
  python separator.py *.mp4 --video-dir videos --audio-dir audio

Output:
  Videos: Saved to videos/ directory (no audio)
  Audio: Saved to audio/ directory (no video)
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input video file(s)'
    )
    
    parser.add_argument(
        '--video-dir',
        default='videos',
        help='Output directory for video files (default: videos/)'
    )
    
    parser.add_argument(
        '--audio-dir',
        default='audio',
        help='Output directory for audio files (default: audio/)'
    )
    
    parser.add_argument(
        '--video-format',
        default='mp4',
        choices=['mp4', 'mkv', 'avi', 'mov', 'webm'],
        help='Output video format (default: mp4)'
    )
    
    parser.add_argument(
        '--audio-format',
        default='mp3',
        choices=['mp3', 'wav', 'aac', 'm4a', 'flac', 'ogg'],
        help='Output audio format (default: mp3)'
    )
    
    args = parser.parse_args()
    
    # Initialize separator
    try:
        separator = MediaSeparator(
            video_dir=args.video_dir,
            audio_dir=args.audio_dir
        )
        separator.check_ffmpeg()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate input files
    input_files = []
    for pattern in args.input:
        path = Path(pattern)
        if path.is_file():
            input_files.append(str(path))
        else:
            print(f"Warning: Skipping {pattern} (not a file)")
    
    if not input_files:
        print("Error: No valid input files found", file=sys.stderr)
        sys.exit(1)
    
    # Process files
    if len(input_files) == 1:
        result = separator.separate_file(
            input_files[0],
            video_format=args.video_format,
            audio_format=args.audio_format
        )
        sys.exit(0 if result['status'] == 'success' else 1)
    else:
        results = separator.separate_batch(
            input_files,
            video_format=args.video_format,
            audio_format=args.audio_format
        )
        sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
