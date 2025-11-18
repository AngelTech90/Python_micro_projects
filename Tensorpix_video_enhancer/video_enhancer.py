#!/usr/bin/env python3
"""
TensorPix Video Enhancer
AI-powered video upscaling and enhancement using TensorPix API
"""

import requests
import time
import sys
import os
from pathlib import Path
from typing import List, Optional, Dict
import argparse
import json


class TensorPixEnhancer:
    """TensorPix API client for video enhancement"""
    
    BASE_URL = "https://api.tensorpix.ai/api/v1"
    
    # Enhancement settings as specified
    ENHANCEMENT_SETTINGS = {
        "upscale": "1080p",      # 1080p Full HD
        "preset": "people",       # People preset
        "framerate": 60,          # 60 FPS
        "ai_upscale": "2x_4"     # 2x Upscale 4
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TENSORPIX_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TensorPix API key required.\n"
                "Set TENSORPIX_API_KEY environment variable or pass api_key parameter.\n"
                "Get your key at: https://tensorpix.ai/"
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def upload_video(self, file_path: str) -> str:
        """Upload video file to TensorPix"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Supported formats
        supported = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
        if file_path.suffix.lower() not in supported:
            raise ValueError(
                f"Unsupported format: {file_path.suffix}\n"
                f"Supported: {', '.join(supported)}"
            )
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"  Uploading: {file_path.name} ({file_size_mb:.2f} MB)")
        
        # Step 1: Request upload URL
        response = self.session.post(
            f"{self.BASE_URL}/upload/request",
            json={"filename": file_path.name},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        upload_url = data['upload_url']
        video_id = data['video_id']
        
        # Step 2: Upload to signed URL
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                data=f,
                headers={'Content-Type': 'video/mp4'},
                timeout=600
            )
            upload_response.raise_for_status()
        
        print(f"  ✓ Uploaded: {video_id}")
        return video_id
    
    def start_enhancement(self, video_id: str) -> str:
        """Start video enhancement with specified settings"""
        payload = {
            "video_id": video_id,
            "settings": {
                "resolution": self.ENHANCEMENT_SETTINGS["upscale"],
                "preset": self.ENHANCEMENT_SETTINGS["preset"],
                "fps": self.ENHANCEMENT_SETTINGS["framerate"],
                "upscale_model": self.ENHANCEMENT_SETTINGS["ai_upscale"],
                "denoise": True,
                "sharpen": True,
                "color_enhance": True
            }
        }
        
        print(f"  Enhancement settings:")
        print(f"    Resolution: 1080p Full HD")
        print(f"    Preset: People")
        print(f"    Framerate: 60 FPS")
        print(f"    AI Upscale: 2x Upscale 4")
        
        response = self.session.post(
            f"{self.BASE_URL}/enhance",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        
        job_id = response.json()['job_id']
        print(f"  Enhancement started: {job_id}")
        return job_id
    
    def get_status(self, job_id: str) -> Dict:
        """Get enhancement job status"""
        response = self.session.get(
            f"{self.BASE_URL}/status/{job_id}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, job_id: str, timeout: int = 3600) -> str:
        """
        Wait for enhancement to complete
        Note: Video processing can take 10-30 minutes per minute of video
        """
        print("  Processing (this may take 10-30 min per video minute)...")
        start_time = time.time()
        last_progress = -1
        
        while time.time() - start_time < timeout:
            data = self.get_status(job_id)
            status = data['status']
            progress = data.get('progress', 0)
            
            # Show progress updates
            if progress != last_progress and progress > 0:
                elapsed = (time.time() - start_time) / 60
                print(f"    Progress: {progress}% (elapsed: {elapsed:.1f} min)")
                last_progress = progress
            
            if status == 'completed':
                total_time = (time.time() - start_time) / 60
                print(f"  ✓ Complete! (took {total_time:.1f} minutes)")
                return data['download_url']
            
            elif status == 'failed':
                error = data.get('error', 'Unknown error')
                raise Exception(f"Enhancement failed: {error}")
            
            elif status in ['processing', 'queued']:
                time.sleep(15)  # Check every 15 seconds
            else:
                raise Exception(f"Unknown status: {status}")
        
        raise TimeoutError(f"Enhancement timeout after {timeout} seconds")
    
    def download_video(self, url: str, output_path: str):
        """Download enhanced video"""
        print(f"  Downloading to: {output_path}")
        
        response = requests.get(url, stream=True, timeout=600)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"    Download: {progress:.1f}%", end='\r')
        
        print(f"\n  ✓ Saved: {output_path}")
    
    def enhance_video(self, input_path: str, output_path: str) -> bool:
        """Complete enhancement workflow for single video"""
        print(f"\n{'='*60}")
        print(f"Processing: {Path(input_path).name}")
        print(f"Target: 1080p @ 60fps, People Preset, 2x Upscale 4")
        print('='*60)
        
        try:
            video_id = self.upload_video(input_path)
            job_id = self.start_enhancement(video_id)
            download_url = self.wait_for_completion(job_id)
            self.download_video(download_url, output_path)
            
            print(f"✓ Success: {output_path}\n")
            return True
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}\n")
            return False
    
    def enhance_batch(self, input_files: List[str], output_dir: str) -> Dict:
        """Enhance multiple video files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING: {len(input_files)} videos")
        print(f"Output directory: {output_dir}")
        print(f"Settings: 1080p @ 60fps, People, 2x Upscale 4")
        print('='*60)
        
        results = {'success': 0, 'failed': 0, 'files': []}
        
        for i, input_file in enumerate(input_files, 1):
            input_path = Path(input_file)
            output_path = output_dir / f"enhanced_{input_path.stem}.mp4"
            
            print(f"\n[{i}/{len(input_files)}]")
            
            success = self.enhance_video(str(input_path), str(output_path))
            
            results['files'].append({
                'input': str(input_path),
                'output': str(output_path) if success else None,
                'status': 'success' if success else 'failed'
            })
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
        
        # Summary
        print("\n" + "="*60)
        print("BATCH COMPLETE")
        print("="*60)
        print(f"Total: {len(input_files)}")
        print(f"Success: {results['success']}")
        print(f"Failed: {results['failed']}")
        print("="*60 + "\n")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Enhance videos using TensorPix AI (1080p@60fps, People, 2x Upscale 4)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single video
  python tensorpix_enhancer.py input.mp4 -o output.mp4
  
  # Multiple videos
  python tensorpix_enhancer.py video1.mp4 video2.mp4 -o output_dir/
  
  # Batch process
  python tensorpix_enhancer.py *.mp4 -o enhanced/
  
  # With API key
  python tensorpix_enhancer.py input.mp4 -o output.mp4 --api-key YOUR_KEY

Settings (Fixed):
  Resolution: 1080p Full HD
  Preset: People
  Framerate: 60 FPS
  AI Upscale: 2x Upscale 4

Environment:
  TENSORPIX_API_KEY    Your TensorPix API key
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input video file(s)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file or directory'
    )
    
    parser.add_argument(
        '--api-key',
        help='TensorPix API key'
    )
    
    args = parser.parse_args()
    
    # Initialize enhancer
    try:
        enhancer = TensorPixEnhancer(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate input files
    supported = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']
    input_files = []
    
    for pattern in args.input:
        path = Path(pattern)
        if path.is_file() and path.suffix.lower() in supported:
            input_files.append(str(path))
        else:
            print(f"Warning: Skipping {pattern}")
    
    if not input_files:
        print("Error: No valid video files found", file=sys.stderr)
        sys.exit(1)
    
    # Process videos
    if len(input_files) == 1:
        success = enhancer.enhance_video(input_files[0], args.output)
        sys.exit(0 if success else 1)
    else:
        results = enhancer.enhance_batch(input_files, args.output)
        sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
