#!/usr/bin/env python3
"""
Video Transcription and Timestamp Analysis Script
Extracts transcription from video using FFmpeg and analyzes it with Gemini AI
to identify optimal timestamps for complementary video clips.
"""

import os
import sys
import subprocess
import pickle
import json
import re
from pathlib import Path
import google.generativeai as genai
from datetime import datetime


class VideoTimestampAnalyzer:
    def __init__(self, api_key, video_path):
        """
        Initialize the analyzer with Gemini API key and video path.
        
        Args:
            api_key (str): Google Gemini API key
            video_path (str): Path to the video file
        """
        self.api_key = api_key
        self.video_path = Path(video_path)
        self.transcription_dir = Path("transcriptions")
        self.dataset_dir = Path("data_sets")
        
        # Create directories if they don't exist
        self.transcription_dir.mkdir(exist_ok=True)
        self.dataset_dir.mkdir(exist_ok=True)
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Generate output filenames based on video name
        video_name = self.video_path.stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.transcription_file = self.transcription_dir / f"{video_name}_{timestamp}.txt"
        self.pkl_file = self.dataset_dir / f"{video_name}_{timestamp}_timestamps.pkl"
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed and accessible."""
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
            print("Please install FFmpeg: sudo apt-get install ffmpeg")
            return False
    
    def extract_transcription(self):
        """
        Extract transcription with timestamps from video using FFmpeg.
        This extracts subtitles if available in the video file.
        """
        print(f"\n[1/3] Extracting transcription from: {self.video_path}")
        
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        
        # Try to extract embedded subtitles first
        try:
            # Extract subtitle track (if available)
            subtitle_temp = self.transcription_dir / "temp_subtitle.srt"
            
            cmd = [
                "ffmpeg",
                "-i", str(self.video_path),
                "-map", "0:s:0",  # Select first subtitle stream
                "-f", "srt",
                str(subtitle_temp),
                "-y"
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if subtitle_temp.exists() and subtitle_temp.stat().st_size > 0:
                # Read and format subtitles
                with open(subtitle_temp, 'r', encoding='utf-8') as f:
                    subtitle_content = f.read()
                
                # Convert SRT to readable format with timestamps
                transcription = self._format_srt_to_text(subtitle_content)
                
                # Save transcription
                with open(self.transcription_file, 'w', encoding='utf-8') as f:
                    f.write(transcription)
                
                # Clean up temp file
                subtitle_temp.unlink()
                
                print(f"✓ Transcription extracted successfully")
                print(f"  Saved to: {self.transcription_file}")
                return True
            
        except Exception as e:
            print(f"Note: No embedded subtitles found or extraction failed")
        
        # If subtitle extraction failed, create a basic audio transcription placeholder
        print("Creating audio-based transcription placeholder...")
        print("Note: For actual speech-to-text, consider using Whisper or similar STT services")
        
        # Extract audio duration and create a basic transcription template
        duration = self._get_video_duration()
        
        placeholder_text = f"""[Transcription Template]
Video: {self.video_path.name}
Duration: {duration}

[00:00:00] Video starts
[Note: This is a placeholder. For actual transcription, please use:
 - Manual transcription
 - YouTube auto-generated captions (if applicable)
 - Whisper AI: https://github.com/openai/whisper
 - Other speech-to-text services]

Please replace this content with actual transcription including timestamps in format [HH:MM:SS] text
"""
        
        with open(self.transcription_file, 'w', encoding='utf-8') as f:
            f.write(placeholder_text)
        
        print(f"✓ Transcription template created: {self.transcription_file}")
        print("  Please add actual transcription content before running analysis")
        return True
    
    def _get_video_duration(self):
        """Get video duration using ffprobe."""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(self.video_path)
            ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            duration_seconds = float(result.stdout.strip())
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)
            
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception as e:
            return "Unknown"
    
    def _format_srt_to_text(self, srt_content):
        """Convert SRT subtitle format to readable text with timestamps."""
        lines = srt_content.strip().split('\n')
        formatted_lines = []
        
        i = 0
        while i < len(lines):
            # Skip subtitle index numbers
            if lines[i].strip().isdigit():
                i += 1
                continue
            
            # Process timestamp line
            if '-->' in lines[i]:
                timestamp_line = lines[i].strip()
                start_time = timestamp_line.split('-->')[0].strip().split(',')[0]
                
                # Get subtitle text (may span multiple lines)
                i += 1
                subtitle_text = []
                while i < len(lines) and lines[i].strip() and not lines[i].strip().isdigit():
                    subtitle_text.append(lines[i].strip())
                    i += 1
                
                if subtitle_text:
                    formatted_lines.append(f"[{start_time}] {' '.join(subtitle_text)}")
            else:
                i += 1
        
        return '\n'.join(formatted_lines)
    
    def analyze_with_gemini(self):
        """
        Send transcription to Gemini AI for analysis and extract timestamp dictionary.
        """
        print(f"\n[2/3] Analyzing transcription with Gemini AI...")
        
        # Read transcription
        with open(self.transcription_file, 'r', encoding='utf-8') as f:
            transcription = f.read()
        
        # Prepare the prompt
        prompt = f"""Use this video transcription as reference to find the time stamps in video that can be convenient to add a clip with some video that complements information of that part of video. If I'm talking about a car model, get the start time stamp and end time stamp to add a short video that complements what I'm talking about. Do this for max 11 parts of my video.

Then, return only and absolutely nothing more than a dictionary in Python with adapted time stamps to then be processed with FFMPEG for adding specific videos with this structure:

{{"complementary_video_stamps": ("12:34", "12:40")}}

Being in the dictionary a reference name to that complementary video that we want to add, then a tuple where first element is start time stamp and second is end timestamp.

IMPORTANT: Return ONLY the Python dictionary, no explanation, no markdown formatting, no code blocks. Just the raw dictionary.

Video Transcription:
{transcription}
"""
        
        try:
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            print("✓ Received response from Gemini AI")
            
            # Extract and parse the dictionary
            timestamps_dict = self._extract_dictionary(response_text)
            
            if timestamps_dict:
                print(f"✓ Successfully parsed {len(timestamps_dict)} timestamp entries")
                return timestamps_dict
            else:
                print("✗ Failed to parse valid dictionary from response")
                print("Raw response:")
                print(response_text)
                return None
            
        except Exception as e:
            print(f"✗ Error during Gemini AI analysis: {e}")
            return None
    
    def _extract_dictionary(self, text):
        """
        Extract Python dictionary from AI response text.
        Handles various formatting issues.
        """
        # Remove markdown code blocks if present
        text = re.sub(r'```python\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        try:
            # Try to evaluate as Python literal
            result = eval(text)
            if isinstance(result, dict):
                return result
        except Exception as e:
            print(f"Direct eval failed: {e}")
        
        # Try to find dictionary pattern in text
        dict_pattern = r'\{[^}]+\}'
        matches = re.finditer(dict_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                potential_dict = eval(match.group())
                if isinstance(potential_dict, dict):
                    return potential_dict
            except:
                continue
        
        return None
    
    def save_to_pickle(self, data):
        """
        Save the timestamp dictionary to a pickle file.
        
        Args:
            data (dict): Timestamp dictionary to save
        """
        print(f"\n[3/3] Saving results to pickle file...")
        
        if data is None:
            print("✗ No data to save")
            return False
        
        try:
            with open(self.pkl_file, 'wb') as f:
                pickle.dump(data, f)
            
            print(f"✓ Data saved successfully")
            print(f"  Saved to: {self.pkl_file}")
            
            # Also save as JSON for easy viewing
            json_file = self.pkl_file.with_suffix('.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  JSON copy: {json_file}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving pickle file: {e}")
            return False
    
    def run_full_pipeline(self):
        """Execute the complete pipeline."""
        print("=" * 60)
        print("Video Timestamp Analyzer - Gemini AI Integration")
        print("=" * 60)
        
        # Check FFmpeg
        if not self.check_ffmpeg():
            return False
        
        # Extract transcription
        if not self.extract_transcription():
            return False
        
        # Analyze with Gemini
        timestamps = self.analyze_with_gemini()
        
        if timestamps is None:
            print("\n✗ Pipeline failed at analysis stage")
            return False
        
        # Save results
        if not self.save_to_pickle(timestamps):
            return False
        
        print("\n" + "=" * 60)
        print("✓ Pipeline completed successfully!")
        print("=" * 60)
        print(f"\nOutput files:")
        print(f"  - Transcription: {self.transcription_file}")
        print(f"  - Timestamps:    {self.pkl_file}")
        print(f"  - JSON:          {self.pkl_file.with_suffix('.json')}")
        
        return True


def main():
    """Main entry point for the script."""
    print("\n" + "=" * 60)
    print("Video Timestamp Analyzer")
    print("=" * 60 + "\n")
    
    # Get API key from environment variable or prompt
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        print("\nOr pass it as first argument:")
        print("  python extract_and_analyze_timestamps.py API_KEY VIDEO_PATH")
        sys.exit(1)
    
    # Get video path
    if len(sys.argv) < 2:
        print("Usage: python extract_and_analyze_timestamps.py [API_KEY] VIDEO_PATH")
        print("\nExample:")
        print("  python extract_and_analyze_timestamps.py my_video.mp4")
        print("  python extract_and_analyze_timestamps.py YOUR_API_KEY my_video.mp4")
        sys.exit(1)
    
    # Check if first arg is API key or video path
    if len(sys.argv) == 3:
        api_key = sys.argv[1]
        video_path = sys.argv[2]
    else:
        video_path = sys.argv[1]
    
    # Run the analyzer
    analyzer = VideoTimestampAnalyzer(api_key, video_path)
    success = analyzer.run_full_pipeline()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
