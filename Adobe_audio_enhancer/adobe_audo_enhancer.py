#!/usr/bin/env python3
"""
Adobe Podcast Audio Enhancer
Enhance single or multiple MP3 files using Adobe's AI
"""

import requests
import time
import sys
import os
from pathlib import Path
from typing import List, Optional
import argparse
import json


class AdobeAudioEnhancer:
    """Adobe Podcast API client for audio enhancement"""
    
    BASE_URL = "https://podcast.adobe.com/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ADOBE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Adobe API key required.\n"
                "Set ADOBE_API_KEY environment variable or pass api_key parameter.\n"
                "Get your key at: https://podcast.adobe.com/"
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def upload_file(self, file_path: str) -> str:
        """Upload MP3 file to Adobe servers"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if file_path.suffix.lower() != '.mp3':
            raise ValueError(f"Only MP3 files supported. Got: {file_path.suffix}")
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"  Uploading: {file_path.name} ({file_size_mb:.2f} MB)")
        
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'audio/mpeg')}
            response = self.session.post(
                f"{self.BASE_URL}/upload",
                files=files,
                timeout=300
            )
        
        response.raise_for_status()
        upload_id = response.json()['upload_id']
        print(f"  ✓ Uploaded: {upload_id}")
        return upload_id
    
    def start_enhancement(self, upload_id: str) -> str:
        """Request audio enhancement"""
        payload = {
            "upload_id": upload_id,
            "enhancement": "speech",
            "noise_reduction": True,
            "normalize": True
        }
        
        response = self.session.post(
            f"{self.BASE_URL}/enhance",
            json=payload,
            timeout=60
        )
        
        response.raise_for_status()
        job_id = response.json()['job_id']
        print(f"  Enhancement started: {job_id}")
        return job_id
    
    def wait_for_completion(self, job_id: str, timeout: int = 600) -> str:
        """Wait for enhancement to complete and return download URL"""
        print("  Processing...", end='', flush=True)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self.session.get(
                f"{self.BASE_URL}/status/{job_id}",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            status = data['status']
            
            if status == 'completed':
                print(" Done!")
                return data['download_url']
            elif status == 'failed':
                raise Exception(f"Enhancement failed: {data.get('error')}")
            
            print(".", end='', flush=True)
            time.sleep(5)
        
        raise TimeoutError("Enhancement timeout")
    
    def download_file(self, url: str, output_path: str):
        """Download enhanced audio"""
        print(f"  Downloading to: {output_path}")
        
        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"  ✓ Saved: {output_path}")
    
    def enhance_file(self, input_path: str, output_path: str):
        """Complete enhancement workflow for single file"""
        print(f"\n{'='*60}")
        print(f"Processing: {Path(input_path).name}")
        print('='*60)
        
        try:
            upload_id = self.upload_file(input_path)
            job_id = self.start_enhancement(upload_id)
            download_url = self.wait_for_completion(job_id)
            self.download_file(download_url, output_path)
            
            print(f"✓ Success: {output_path}\n")
            return True
            
        except Exception as e:
            print(f"✗ Failed: {str(e)}\n")
            return False
    
    def enhance_batch(self, input_files: List[str], output_dir: str):
        """Enhance multiple MP3 files"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING: {len(input_files)} files")
        print(f"Output directory: {output_dir}")
        print('='*60)
        
        results = {'success': 0, 'failed': 0, 'files': []}
        
        for i, input_file in enumerate(input_files, 1):
            input_path = Path(input_file)
            output_path = output_dir / f"enhanced_{input_path.name}"
            
            print(f"\n[{i}/{len(input_files)}]")
            
            success = self.enhance_file(str(input_path), str(output_path))
            
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
        description="Enhance MP3 audio files using Adobe Podcast AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  python adobe_enhancer.py input.mp3 -o output.mp3
  
  # Multiple files
  python adobe_enhancer.py file1.mp3 file2.mp3 file3.mp3 -o output_dir/
  
  # Batch process directory
  python adobe_enhancer.py *.mp3 -o enhanced/
  
  # With API key
  python adobe_enhancer.py input.mp3 -o output.mp3 --api-key YOUR_KEY

Environment:
  ADOBE_API_KEY    Your Adobe Podcast API key
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input MP3 file(s)'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output file or directory'
    )
    
    parser.add_argument(
        '--api-key',
        help='Adobe API key'
    )
    
    args = parser.parse_args()
    
    # Initialize enhancer
    try:
        enhancer = AdobeAudioEnhancer(api_key=args.api_key)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate input files
    input_files = []
    for pattern in args.input:
        path = Path(pattern)
        if path.is_file() and path.suffix.lower() == '.mp3':
            input_files.append(str(path))
        else:
            print(f"Warning: Skipping {pattern} (not an MP3 file)")
    
    if not input_files:
        print("Error: No valid MP3 files found", file=sys.stderr)
        sys.exit(1)
    
    # Process files
    if len(input_files) == 1:
        # Single file mode
        success = enhancer.enhance_file(input_files[0], args.output)
        sys.exit(0 if success else 1)
    else:
        # Batch mode
        results = enhancer.enhance_batch(input_files, args.output)
        sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
