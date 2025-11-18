#!/usr/bin/env python3
"""
Video Integration Script with FFmpeg
Integrates complementary videos into main video at specified timestamps
using AI-assisted video matching and duration adjustment.
"""

import os
import sys
import subprocess
import pickle
import json
import re
from pathlib import Path
from datetime import datetime
import google.generativeai as genai


class VideoIntegrator:
    def __init__(self, gemini_api_key, original_video, pkl_file, complementary_dir):
        """
        Initialize the video integrator.
        
        Args:
            gemini_api_key (str): Google Gemini API key
            original_video (str): Path to original video file
            pkl_file (str): Path to timestamps pickle file
            complementary_dir (str): Directory with complementary videos
        """
        self.gemini_api_key = gemini_api_key
        self.original_video = Path(original_video)
        self.pkl_file = Path(pkl_file)
        self.complementary_dir = Path(complementary_dir)
        
        # Configure Gemini API
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Data containers
        self.timestamps_data = {}
        self.video_files = []
        self.sorted_videos = []
        self.video_durations = []
        self.ideal_durations = []
        
        # Output directory for final video
        self.output_dir = Path("final_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed."""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            print("✓ FFmpeg is installed and accessible")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("✗ FFmpeg is not installed or not in PATH")
            return False
    
    def load_timestamps(self):
        """Load timestamp data from pickle file."""
        print(f"\n[1/7] Loading timestamp data from: {self.pkl_file}")
        
        if not self.pkl_file.exists():
            raise FileNotFoundError(f"Pickle file not found: {self.pkl_file}")
        
        try:
            with open(self.pkl_file, 'rb') as f:
                self.timestamps_data = pickle.load(f)
            
            print(f"✓ Loaded {len(self.timestamps_data)} timestamp entries")
            print("\nTimestamp entries:")
            for idx, (key, timestamps) in enumerate(self.timestamps_data.items(), 1):
                print(f"  {idx}. {key}: {timestamps[0]} → {timestamps[1]}")
            
            return True
        except Exception as e:
            print(f"✗ Error loading pickle file: {e}")
            return False
    
    def extract_video_files(self):
        """Extract list of video files from complementary directory."""
        print(f"\n[2/7] Extracting video files from: {self.complementary_dir}")
        
        if not self.complementary_dir.exists():
            print(f"✗ Directory not found: {self.complementary_dir}")
            return False
        
        # Get all .mp4 files
        self.video_files = sorted([
            f.name for f in self.complementary_dir.glob("*.mp4")
        ])
        
        if not self.video_files:
            print("✗ No .mp4 files found in directory")
            return False
        
        print(f"✓ Found {len(self.video_files)} video files")
        print("\nVideo files:")
        for idx, video in enumerate(self.video_files, 1):
            print(f"  {idx}. {video}")
        
        return True
    
    def sort_videos_with_gemini(self):
        """Use Gemini to match and sort video files with timestamp keys."""
        print(f"\n[3/7] Matching videos with timestamps using Gemini AI...")
        
        # Prepare data for Gemini
        timestamp_keys = list(self.timestamps_data.keys())
        
        prompt = f"""You have a list of video filenames and a list of timestamp keys. Your task is to match each video filename with its corresponding timestamp key and return them in the correct order.

Timestamp Keys (in order):
{json.dumps(timestamp_keys, indent=2)}

Video Filenames:
{json.dumps(self.video_files, indent=2)}

The video filenames follow the pattern: ##_key_name.mp4 where ## is a number prefix.

IMPORTANT: Return ONLY a Python list of video filenames in the exact order that matches the timestamp keys order. No explanation, no markdown, no code blocks. Just the raw Python list.

Example output format:
["01_first_key.mp4", "02_second_key.mp4", "03_third_key.mp4"]

Return the sorted list now:"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            print("✓ Received response from Gemini AI")
            
            # Parse the list
            self.sorted_videos = self._extract_list(response_text)
            
            if self.sorted_videos and len(self.sorted_videos) == len(timestamp_keys):
                print(f"✓ Successfully sorted {len(self.sorted_videos)} videos")
                print("\nSorted video order:")
                for idx, (key, video) in enumerate(zip(timestamp_keys, self.sorted_videos), 1):
                    print(f"  {idx}. {key} → {video}")
                return True
            else:
                print("✗ Failed to sort videos properly")
                if self.sorted_videos:
                    print(f"Expected {len(timestamp_keys)} videos, got {len(self.sorted_videos)}")
                return False
                
        except Exception as e:
            print(f"✗ Error sorting videos: {e}")
            return False
    
    def extract_video_durations(self):
        """Extract duration of each complementary video using FFmpeg."""
        print(f"\n[4/7] Extracting video durations with FFmpeg...")
        
        self.video_durations = []
        
        for idx, video_name in enumerate(self.sorted_videos, 1):
            video_path = self.complementary_dir / video_name
            
            if not video_path.exists():
                print(f"  ✗ Video not found: {video_name}")
                return False
            
            try:
                # Use ffprobe to get duration
                cmd = [
                    "ffprobe",
                    "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(video_path)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                
                duration_seconds = float(result.stdout.strip())
                self.video_durations.append(duration_seconds)
                
                print(f"  {idx}. {video_name}: {duration_seconds:.2f}s")
                
            except Exception as e:
                print(f"  ✗ Error getting duration for {video_name}: {e}")
                return False
        
        print(f"✓ Extracted durations for all {len(self.video_durations)} videos")
        return True
    
    def calculate_ideal_durations_with_gemini(self):
        """Use Gemini to calculate ideal durations based on timestamps."""
        print(f"\n[5/7] Calculating ideal durations with Gemini AI...")
        
        # Prepare timestamp durations
        timestamp_keys = list(self.timestamps_data.keys())
        timestamp_durations = []
        
        for key in timestamp_keys:
            start, end = self.timestamps_data[key]
            duration = self._timestamp_to_seconds(end) - self._timestamp_to_seconds(start)
            timestamp_durations.append(duration)
        
        # Create comparison data
        comparison_data = []
        for idx, (video, video_dur, ts_dur) in enumerate(
            zip(self.sorted_videos, self.video_durations, timestamp_durations), 1
        ):
            comparison_data.append({
                "index": idx,
                "video": video,
                "video_duration": video_dur,
                "required_duration": ts_dur,
                "needs_cutting": video_dur > ts_dur
            })
        
        prompt = f"""You have complementary videos with their current durations and required durations based on timestamps. For videos that are longer than required, you need to determine the ideal duration to cut them to.

Video Duration Comparison:
{json.dumps(comparison_data, indent=2)}

For each video, return the ideal duration in seconds. Rules:
1. If video_duration <= required_duration: keep original duration
2. If video_duration > required_duration: use required_duration
3. Return durations as float numbers (e.g., 25.5, 30.0, 15.75)

IMPORTANT: Return ONLY a Python list of durations (float numbers in seconds) in the same order as the input. No explanation, no markdown, no code blocks. Just the raw Python list.

Example output format:
[30.0, 25.5, 20.0, 15.75, 28.0]

Return the ideal durations list now:"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            print("✓ Received response from Gemini AI")
            
            # Parse the list
            self.ideal_durations = self._extract_list(response_text)
            
            if self.ideal_durations and len(self.ideal_durations) == len(self.sorted_videos):
                print(f"✓ Successfully calculated ideal durations")
                print("\nDuration adjustments:")
                for idx, (video, orig_dur, ideal_dur) in enumerate(
                    zip(self.sorted_videos, self.video_durations, self.ideal_durations), 1
                ):
                    if orig_dur > ideal_dur:
                        print(f"  {idx}. {video}: {orig_dur:.2f}s → {ideal_dur:.2f}s (CUT)")
                    else:
                        print(f"  {idx}. {video}: {orig_dur:.2f}s (NO CHANGE)")
                return True
            else:
                print("✗ Failed to calculate ideal durations")
                return False
                
        except Exception as e:
            print(f"✗ Error calculating durations: {e}")
            return False
    
    def trim_videos_with_ffmpeg(self):
        """Trim videos to ideal durations using FFmpeg."""
        print(f"\n[6/7] Trimming videos to ideal durations with FFmpeg...")
        
        for idx, (video_name, ideal_dur) in enumerate(
            zip(self.sorted_videos, self.ideal_durations), 1
        ):
            video_path = self.complementary_dir / video_name
            
            # Only trim if needed
            if self.video_durations[idx - 1] <= ideal_dur:
                print(f"  {idx}. {video_name}: No trimming needed")
                continue
            
            print(f"  {idx}. {video_name}: Trimming to {ideal_dur:.2f}s...")
            
            # Create temporary output file
            temp_output = self.complementary_dir / f"temp_{video_name}"
            
            try:
                # FFmpeg command to trim video
                cmd = [
                    "ffmpeg",
                    "-i", str(video_path),
                    "-t", str(ideal_dur),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-strict", "experimental",
                    "-b:a", "192k",
                    "-y",
                    str(temp_output)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if result.returncode == 0 and temp_output.exists():
                    # Replace original with trimmed version
                    video_path.unlink()
                    temp_output.rename(video_path)
                    print(f"    ✓ Trimmed successfully")
                else:
                    print(f"    ✗ Trimming failed")
                    if temp_output.exists():
                        temp_output.unlink()
                    return False
                    
            except Exception as e:
                print(f"    ✗ Error trimming video: {e}")
                if temp_output.exists():
                    temp_output.unlink()
                return False
        
        print("✓ All videos trimmed successfully")
        return True
    
    def integrate_videos_with_ffmpeg(self):
        """Integrate complementary videos into main video using FFmpeg."""
        print(f"\n[7/7] Integrating complementary videos into main video...")
        
        if not self.original_video.exists():
            print(f"✗ Original video not found: {self.original_video}")
            return False
        
        # Prepare output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"final_video_{timestamp}.mp4"
        
        # Build complex FFmpeg filter
        print("  Building FFmpeg filter chain...")
        
        # Get all video inputs
        inputs = ["-i", str(self.original_video)]
        for video_name in self.sorted_videos:
            video_path = self.complementary_dir / video_name
            inputs.extend(["-i", str(video_path)])
        
        # Build filter_complex for video overlay
        timestamp_keys = list(self.timestamps_data.keys())
        filter_parts = []
        
        # Start with main video
        current_video = "[0:v]"
        
        for idx, (key, video_name) in enumerate(zip(timestamp_keys, self.sorted_videos), 1):
            start_time, _ = self.timestamps_data[key]
            start_seconds = self._timestamp_to_seconds(start_time)
            
            # Scale complementary video to match main video
            filter_parts.append(f"[{idx}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v{idx}]")
            
            # Overlay at specific timestamp
            if idx == 1:
                filter_parts.append(f"{current_video}[v{idx}]overlay=0:0:enable='between(t,{start_seconds},{start_seconds + self.ideal_durations[idx-1]})'[tmp{idx}]")
            else:
                filter_parts.append(f"[tmp{idx-1}][v{idx}]overlay=0:0:enable='between(t,{start_seconds},{start_seconds + self.ideal_durations[idx-1]})'[tmp{idx}]")
            
            current_video = f"[tmp{idx}]"
        
        # Final output mapping
        if filter_parts:
            filter_complex = ";".join(filter_parts)
            final_output = f"[tmp{len(timestamp_keys)}]"
        else:
            filter_complex = ""
            final_output = "[0:v]"
        
        print("  Executing FFmpeg integration (this may take several minutes)...")
        
        try:
            # Build complete FFmpeg command
            cmd = ["ffmpeg"] + inputs
            
            if filter_complex:
                cmd.extend([
                    "-filter_complex", filter_complex,
                    "-map", final_output.strip("[]"),
                    "-map", "0:a"
                ])
            else:
                cmd.extend(["-map", "0:v", "-map", "0:a"])
            
            cmd.extend([
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",
                str(output_file)
            ])
            
            # Execute FFmpeg
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0 and output_file.exists():
                print(f"✓ Video integration completed successfully!")
                print(f"  Output: {output_file}")
                
                # Get output file size
                file_size_mb = output_file.stat().st_size / (1024 * 1024)
                print(f"  Size: {file_size_mb:.2f} MB")
                
                return True
            else:
                print("✗ Video integration failed")
                print("FFmpeg error output:")
                print(result.stderr[-2000:])  # Last 2000 chars
                return False
                
        except Exception as e:
            print(f"✗ Error during integration: {e}")
            return False
    
    def _timestamp_to_seconds(self, timestamp):
        """Convert timestamp string to seconds."""
        parts = timestamp.split(':')
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    
    def _extract_list(self, text):
        """Extract Python list from AI response text."""
        # Remove markdown code blocks
        text = re.sub(r'```python\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        try:
            result = eval(text)
            if isinstance(result, list):
                return result
        except Exception as e:
            print(f"Direct eval failed: {e}")
        
        # Try to find list pattern
        list_pattern = r'\[.*?\]'
        matches = re.finditer(list_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                potential_list = eval(match.group())
                if isinstance(potential_list, list):
                    return potential_list
            except:
                continue
        
        return None
    
    def run_full_pipeline(self):
        """Execute the complete integration pipeline."""
        print("=" * 70)
        print("Video Integration Pipeline - FFmpeg + Gemini AI")
        print("=" * 70)
        
        # Check FFmpeg
        if not self.check_ffmpeg():
            return False
        
        # Load timestamps
        if not self.load_timestamps():
            return False
        
        # Extract video files
        if not self.extract_video_files():
            return False
        
        # Sort videos with Gemini
        if not self.sort_videos_with_gemini():
            return False
        
        # Extract video durations
        if not self.extract_video_durations():
            return False
        
        # Calculate ideal durations
        if not self.calculate_ideal_durations_with_gemini():
            return False
        
        # Trim videos
        if not self.trim_videos_with_ffmpeg():
            return False
        
        # Integrate videos
        if not self.integrate_videos_with_ffmpeg():
            return False
        
        print("\n" + "=" * 70)
        print("✓ Pipeline completed successfully!")
        print("=" * 70)
        
        return True


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("Video Integration Script")
    print("=" * 70 + "\n")
    
    # Get Gemini API key
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Get command line arguments
    if len(sys.argv) < 4:
        print("Usage: python integrate_complementary_videos.py ORIGINAL_VIDEO PKL_FILE COMPLEMENTARY_DIR")
        print("\nExample:")
        print("  python integrate_complementary_videos.py my_video.mp4 \\")
        print("         data_sets/video_20241115_143022_timestamps.pkl \\")
        print("         complementary_videos/")
        sys.exit(1)
    
    original_video = sys.argv[1]
    pkl_file = sys.argv[2]
    complementary_dir = sys.argv[3]
    
    # Run integrator
    integrator = VideoIntegrator(
        gemini_api_key,
        original_video,
        pkl_file,
        complementary_dir
    )
    
    success = integrator.run_full_pipeline()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
