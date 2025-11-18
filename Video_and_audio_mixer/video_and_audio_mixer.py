#!/usr/bin/env python3
"""
Video/Audio Mixer
Mix separate video and audio files into a single MP4 file using FFmpeg
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional, Dict
import argparse
import json


class MediaMixer:
    """Mix video and audio streams using FFmpeg"""
    
    def __init__(self):
        """Initialize mixer"""
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "FFmpeg not found. Install it:\n"
                "  Ubuntu/Debian: sudo apt install ffmpeg\n"
                "  Fedora: sudo dnf install ffmpeg\n"
                "  macOS: brew install ffmpeg"
            )
    
    def get_duration(self, file_path: str) -> float:
        """Get media file duration in seconds"""
        try:
            result = subprocess.run([
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                file_path
            ], capture_output=True, text=True, check=True)
            
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except Exception:
            return 0.0
    
    def mix_simple(
        self,
        video_file: str,
        audio_file: str,
        output_file: str,
        video_codec: str = 'copy',
        audio_codec: str = 'aac',
        audio_bitrate: str = '320k'
    ):
        """
        Simple mix: Replace video's audio with new audio
        
        Args:
            video_file: Input video file (can have or not have audio)
            audio_file: Input audio file
            output_file: Output video file
            video_codec: Video codec ('copy' for no re-encoding)
            audio_codec: Audio codec (default: aac)
            audio_bitrate: Audio bitrate (default: 320k)
        """
        print(f"  Video: {Path(video_file).name}")
        print(f"  Audio: {Path(audio_file).name}")
        print(f"  Output: {Path(output_file).name}")
        
        # Get durations
        video_duration = self.get_duration(video_file)
        audio_duration = self.get_duration(audio_file)
        
        print(f"  Video duration: {video_duration:.2f}s")
        print(f"  Audio duration: {audio_duration:.2f}s")
        
        if abs(video_duration - audio_duration) > 1.0:
            print(f"  ⚠ Warning: Duration mismatch ({abs(video_duration - audio_duration):.2f}s difference)")
        
        # Mix command
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-c:v', video_codec,
            '-c:a', audio_codec,
        ]
        
        if audio_codec != 'copy':
            cmd.extend(['-b:a', audio_bitrate])
        
        cmd.extend([
            '-map', '0:v:0',      # Video from first input
            '-map', '1:a:0',      # Audio from second input
            '-shortest',          # End when shortest stream ends
            '-y',                 # Overwrite output
            output_file
        ])
        
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  ✓ Mixed successfully!")
    
    def mix_with_original(
        self,
        video_file: str,
        audio_file: str,
        output_file: str,
        new_audio_volume: float = 1.0,
        original_audio_volume: float = 0.3
    ):
        """
        Mix new audio with video's original audio
        
        Args:
            video_file: Input video file (must have audio)
            audio_file: New audio file to mix
            output_file: Output video file
            new_audio_volume: Volume for new audio (0.0-2.0)
            original_audio_volume: Volume for original audio (0.0-2.0)
        """
        print(f"  Video: {Path(video_file).name}")
        print(f"  New audio: {Path(audio_file).name}")
        print(f"  Output: {Path(output_file).name}")
        print(f"  New audio volume: {new_audio_volume:.1f}x")
        print(f"  Original audio volume: {original_audio_volume:.1f}x")
        
        subprocess.run([
            'ffmpeg',
            '-i', video_file,
            '-i', audio_file,
            '-filter_complex',
            f'[0:a]volume={original_audio_volume}[a0];'
            f'[1:a]volume={new_audio_volume}[a1];'
            f'[a0][a1]amix=inputs=2:duration=shortest[aout]',
            '-map', '0:v:0',
            '-map', '[aout]',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '320k',
            '-y',
            output_file
        ], capture_output=True, check=True)
        
        print(f"  ✓ Mixed successfully!")
    
    def mix_file(
        self,
        video_file: str,
        audio_file: str,
        output_file: str,
        mode: str = 'replace',
        **kwargs
    ) -> Dict:
        """
        Mix video and audio files
        
        Args:
            video_file: Input video file
            audio_file: Input audio file
            output_file: Output file
            mode: 'replace' or 'mix'
            **kwargs: Additional arguments for specific modes
            
        Returns:
            Result dictionary
        """
        video_path = Path(video_file)
        audio_path = Path(audio_file)
        output_path = Path(output_file)
        
        # Validate inputs
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        print(f"\n{'='*60}")
        print(f"MIXING: {mode.upper()} MODE")
        print('='*60)
        
        try:
            if mode == 'replace':
                self.mix_simple(
                    video_file,
                    audio_file,
                    str(output_path),
                    video_codec=kwargs.get('video_codec', 'copy'),
                    audio_codec=kwargs.get('audio_codec', 'aac'),
                    audio_bitrate=kwargs.get('audio_bitrate', '320k')
                )
            elif mode == 'mix':
                self.mix_with_original(
                    video_file,
                    audio_file,
                    str(output_path),
                    new_audio_volume=kwargs.get('new_volume', 1.0),
                    original_audio_volume=kwargs.get('original_volume', 0.3)
                )
            else:
                raise ValueError(f"Unknown mode: {mode}")
            
            print(f"\n✓ Success: {output_path}\n")
            
            return {
                'video': video_file,
                'audio': audio_file,
                'output': str(output_path),
                'mode': mode,
                'status': 'success'
            }
            
        except Exception as e:
            print(f"\n✗ Failed: {str(e)}\n")
            return {
                'video': video_file,
                'audio': audio_file,
                'output': str(output_path),
                'mode': mode,
                'status': 'failed',
                'error': str(e)
            }
    
    def mix_batch(
        self,
        video_audio_pairs: list,
        output_dir: str,
        mode: str = 'replace',
        **kwargs
    ) -> Dict:
        """
        Mix multiple video-audio pairs
        
        Args:
            video_audio_pairs: List of (video_file, audio_file) tuples
            output_dir: Output directory
            mode: 'replace' or 'mix'
            **kwargs: Additional arguments
            
        Returns:
            Summary dictionary
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"BATCH MIXING: {len(video_audio_pairs)} pairs")
        print(f"Mode: {mode.upper()}")
        print(f"Output directory: {output_dir}/")
        print('='*60)
        
        results = {
            'success': 0,
            'failed': 0,
            'files': []
        }
        
        for i, (video_file, audio_file) in enumerate(video_audio_pairs, 1):
            video_name = Path(video_file).stem
            output_file = output_dir / f"mixed_{video_name}.mp4"
            
            print(f"\n[{i}/{len(video_audio_pairs)}]")
            
            result = self.mix_file(
                video_file,
                audio_file,
                str(output_file),
                mode=mode,
                **kwargs
            )
            
            results['files'].append(result)
            
            if result['status'] == 'success':
                results['success'] += 1
            else:
                results['failed'] += 1
        
        # Summary
        print("\n" + "="*60)
        print("BATCH MIXING COMPLETE")
        print("="*60)
        print(f"Total pairs: {len(video_audio_pairs)}")
        print(f"Success: {results['success']}")
        print(f"Failed: {results['failed']}")
        print(f"Output directory: {output_dir}/")
        print("="*60 + "\n")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Mix video and audio files using FFmpeg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Replace video's audio
  python mixer.py video.mp4 audio.mp3 -o output.mp4
  
  # Mix new audio with original audio
  python mixer.py video.mp4 music.mp3 -o output.mp4 --mode mix
  
  # Custom volume levels
  python mixer.py video.mp4 music.mp3 -o output.mp4 --mode mix \\
      --new-volume 0.8 --original-volume 0.5
  
  # High quality audio codec
  python mixer.py video.mp4 audio.wav -o output.mp4 \\
      --audio-codec flac
  
  # Batch mode: match files from directories
  python mixer.py --batch --video-dir videos/ --audio-dir audio/ -o mixed/

Modes:
  replace (default)  Replace video's audio with new audio
  mix                Mix new audio with video's original audio
        """
    )
    
    # Single file mode arguments
    parser.add_argument(
        'video',
        nargs='?',
        help='Input video file'
    )
    
    parser.add_argument(
        'audio',
        nargs='?',
        help='Input audio file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output video file or directory'
    )
    
    # Mode selection
    parser.add_argument(
        '--mode',
        choices=['replace', 'mix'],
        default='replace',
        help='Mixing mode (default: replace)'
    )
    
    # Audio options
    parser.add_argument(
        '--audio-codec',
        default='aac',
        choices=['aac', 'mp3', 'flac', 'copy'],
        help='Audio codec (default: aac)'
    )
    
    parser.add_argument(
        '--audio-bitrate',
        default='320k',
        help='Audio bitrate (default: 320k)'
    )
    
    # Mix mode options
    parser.add_argument(
        '--new-volume',
        type=float,
        default=1.0,
        help='New audio volume for mix mode (default: 1.0)'
    )
    
    parser.add_argument(
        '--original-volume',
        type=float,
        default=0.3,
        help='Original audio volume for mix mode (default: 0.3)'
    )
    
    # Batch mode
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode: process directories'
    )
    
    parser.add_argument(
        '--video-dir',
        help='Video directory for batch mode'
    )
    
    parser.add_argument(
        '--audio-dir',
        help='Audio directory for batch mode'
    )
    
    args = parser.parse_args()
    
    # Initialize mixer
    try:
        mixer = MediaMixer()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Batch mode
    if args.batch:
        if not args.video_dir or not args.audio_dir or not args.output:
            print("Error: Batch mode requires --video-dir, --audio-dir, and -o", file=sys.stderr)
            sys.exit(1)
        
        video_dir = Path(args.video_dir)
        audio_dir = Path(args.audio_dir)
        
        # Match files by name
        video_files = sorted(video_dir.glob('*.mp4'))
        pairs = []
        
        for video_file in video_files:
            # Look for matching audio file
            audio_file = audio_dir / f"{video_file.stem}.mp3"
            if not audio_file.exists():
                audio_file = audio_dir / f"{video_file.stem}.wav"
            if not audio_file.exists():
                audio_file = audio_dir / f"{video_file.stem}.m4a"
            
            if audio_file.exists():
                pairs.append((str(video_file), str(audio_file)))
            else:
                print(f"Warning: No matching audio for {video_file.name}")
        
        if not pairs:
            print("Error: No matching video-audio pairs found", file=sys.stderr)
            sys.exit(1)
        
        results = mixer.mix_batch(
            pairs,
            args.output,
            mode=args.mode,
            audio_codec=args.audio_codec,
            audio_bitrate=args.audio_bitrate,
            new_volume=args.new_volume,
            original_volume=args.original_volume
        )
        
        sys.exit(0 if results['failed'] == 0 else 1)
    
    # Single file mode
    else:
        if not args.video or not args.audio or not args.output:
            parser.print_help()
            sys.exit(1)
        
        result = mixer.mix_file(
            args.video,
            args.audio,
            args.output,
            mode=args.mode,
            audio_codec=args.audio_codec,
            audio_bitrate=args.audio_bitrate,
            new_volume=args.new_volume,
            original_volume=args.original_volume
        )
        
        sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == "__main__":
    main()
