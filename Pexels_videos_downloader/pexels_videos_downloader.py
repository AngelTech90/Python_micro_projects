#!/usr/bin/env python3
"""
Pexels Complementary Video Downloader
Automatically searches and downloads complementary videos from Pexels
based on timestamp analysis data.
"""

import os
import sys
import pickle
import json
import requests
import time
from pathlib import Path
from urllib.parse import urlparse
import google.generativeai as genai


class PexelsVideoDownloader:
    def __init__(self, pexels_api_key, gemini_api_key, pkl_file_path):
        """
        Initialize the downloader with API keys and pickle file path.
        
        Args:
            pexels_api_key (str): Pexels API key
            gemini_api_key (str): Google Gemini API key
            pkl_file_path (str): Path to the pickle file with timestamps
        """
        self.pexels_api_key = pexels_api_key
        self.gemini_api_key = gemini_api_key
        self.pkl_file_path = Path(pkl_file_path)
        
        # Configure Gemini API
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Create output directory
        self.output_dir = Path("complementary_videos")
        self.output_dir.mkdir(exist_ok=True)
        
        # Pexels API endpoint
        self.pexels_api_url = "https://api.pexels.com/videos/search"
        
        # Load timestamp data
        self.timestamps_data = None
        self.search_queries = []
        self.downloaded_videos = []
    
    def load_pickle_data(self):
        """Load timestamp data from pickle file."""
        print(f"\n[1/4] Loading timestamp data from: {self.pkl_file_path}")
        
        if not self.pkl_file_path.exists():
            raise FileNotFoundError(f"Pickle file not found: {self.pkl_file_path}")
        
        try:
            with open(self.pkl_file_path, 'rb') as f:
                self.timestamps_data = pickle.load(f)
            
            print(f"✓ Loaded {len(self.timestamps_data)} timestamp entries")
            
            # Display loaded data
            print("\nTimestamp entries:")
            for idx, (key, timestamps) in enumerate(self.timestamps_data.items(), 1):
                duration = self._calculate_duration(timestamps[0], timestamps[1])
                print(f"  {idx}. {key}: {timestamps[0]} → {timestamps[1]} ({duration}s)")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading pickle file: {e}")
            return False
    
    def _calculate_duration(self, start_time, end_time):
        """Calculate duration in seconds between two timestamps."""
        def time_to_seconds(time_str):
            parts = time_str.split(':')
            if len(parts) == 2:  # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 3:  # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return 0
        
        start_seconds = time_to_seconds(start_time)
        end_seconds = time_to_seconds(end_time)
        return end_seconds - start_seconds
    
    def generate_search_queries_with_gemini(self):
        """Use Gemini AI to generate search queries for Pexels."""
        print(f"\n[2/4] Generating search queries with Gemini AI...")
        
        if not self.timestamps_data:
            print("✗ No timestamp data loaded")
            return False
        
        # Prepare prompt with timestamp data
        timestamp_info = json.dumps(self.timestamps_data, indent=2)
        
        prompt = f"""Based on this dictionary of video timestamps and their descriptions, generate search queries for finding complementary stock videos on Pexels.

Timestamp Data:
{timestamp_info}

For each entry in the dictionary, create a clear, concise search query (2-4 words) that would find relevant stock footage on Pexels.

IMPORTANT: Return ONLY a Python list of search query strings, nothing else. No explanation, no markdown, no code blocks. Just the raw Python list.

Example output format:
["smartphone unboxing", "phone design closeup", "display screen demo", "camera lens macro"]

Generate the search queries now:"""
        
        try:
            # Generate response
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            print("✓ Received response from Gemini AI")
            
            # Parse the list
            self.search_queries = self._extract_list(response_text)
            
            if self.search_queries:
                print(f"✓ Generated {len(self.search_queries)} search queries")
                print("\nSearch queries:")
                for idx, query in enumerate(self.search_queries, 1):
                    print(f"  {idx}. \"{query}\"")
                return True
            else:
                print("✗ Failed to parse search queries from response")
                print("Raw response:")
                print(response_text)
                return False
                
        except Exception as e:
            print(f"✗ Error generating search queries: {e}")
            return False
    
    def _extract_list(self, text):
        """Extract Python list from AI response text."""
        import re
        
        # Remove markdown code blocks if present
        text = re.sub(r'```python\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        try:
            # Try to evaluate as Python literal
            result = eval(text)
            if isinstance(result, list):
                return result
        except Exception as e:
            print(f"Direct eval failed: {e}")
        
        # Try to find list pattern in text
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
    
    def search_pexels_video(self, query, min_duration):
        """
        Search for a video on Pexels.
        
        Args:
            query (str): Search query
            min_duration (int): Minimum duration in seconds
            
        Returns:
            dict: Video information or None
        """
        headers = {
            "Authorization": self.pexels_api_key
        }
        
        params = {
            "query": query,
            "per_page": 15,  # Get multiple results to find suitable duration
            "orientation": "landscape"
        }
        
        try:
            response = requests.get(
                self.pexels_api_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('videos') and len(data['videos']) > 0:
                    # Find video with suitable duration
                    for video in data['videos']:
                        video_duration = video.get('duration', 0)
                        
                        # Look for video that's at least as long as needed
                        if video_duration >= min_duration:
                            # Get highest quality video file
                            video_files = video.get('video_files', [])
                            if video_files:
                                # Sort by quality (width)
                                video_files.sort(
                                    key=lambda x: x.get('width', 0),
                                    reverse=True
                                )
                                
                                # Prefer HD quality (1280x720 or similar)
                                hd_video = None
                                for vf in video_files:
                                    if vf.get('width', 0) >= 1280:
                                        hd_video = vf
                                        break
                                
                                video_file = hd_video if hd_video else video_files[0]
                                
                                return {
                                    'id': video['id'],
                                    'url': video_file['link'],
                                    'width': video_file.get('width', 0),
                                    'height': video_file.get('height', 0),
                                    'duration': video_duration,
                                    'quality': video_file.get('quality', 'unknown')
                                }
                    
                    # If no video matches duration, return first result anyway
                    video = data['videos'][0]
                    video_files = video.get('video_files', [])
                    if video_files:
                        video_files.sort(
                            key=lambda x: x.get('width', 0),
                            reverse=True
                        )
                        video_file = video_files[0]
                        
                        return {
                            'id': video['id'],
                            'url': video_file['link'],
                            'width': video_file.get('width', 0),
                            'height': video_file.get('height', 0),
                            'duration': video.get('duration', 0),
                            'quality': video_file.get('quality', 'unknown')
                        }
                
                return None
                
            elif response.status_code == 429:
                print("  ⚠ Rate limit reached, waiting 60 seconds...")
                time.sleep(60)
                return self.search_pexels_video(query, min_duration)
            else:
                print(f"  ✗ API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ✗ Search error: {e}")
            return None
    
    def download_video(self, url, output_filename):
        """
        Download a video from URL.
        
        Args:
            url (str): Video URL
            output_filename (str): Output filename
            
        Returns:
            bool: Success status
        """
        try:
            response = requests.get(url, stream=True, timeout=30)
            
            if response.status_code == 200:
                output_path = self.output_dir / output_filename
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # Simple progress indicator
                            if total_size > 0:
                                progress = (downloaded_size / total_size) * 100
                                print(f"\r  Downloading: {progress:.1f}%", end='')
                
                print()  # New line after progress
                return True
            else:
                print(f"  ✗ Download failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ✗ Download error: {e}")
            return False
    
    def download_all_videos(self):
        """Search and download all complementary videos."""
        print(f"\n[3/4] Searching and downloading videos from Pexels...")
        
        if not self.search_queries:
            print("✗ No search queries available")
            return False
        
        # Get timestamp entries as list for matching with queries
        timestamp_items = list(self.timestamps_data.items())
        
        for idx, (query, (original_name, timestamps)) in enumerate(
            zip(self.search_queries, timestamp_items), 1
        ):
            print(f"\n[{idx}/{len(self.search_queries)}] Processing: \"{query}\"")
            print(f"  Original key: {original_name}")
            print(f"  Timestamp: {timestamps[0]} → {timestamps[1]}")
            
            # Calculate required duration
            min_duration = self._calculate_duration(timestamps[0], timestamps[1])
            print(f"  Required duration: {min_duration}s")
            
            # Search for video
            print(f"  Searching Pexels...")
            video_info = self.search_pexels_video(query, min_duration)
            
            if video_info:
                print(f"  ✓ Found video (ID: {video_info['id']})")
                print(f"    Quality: {video_info['width']}x{video_info['height']}")
                print(f"    Duration: {video_info['duration']}s")
                
                # Generate output filename
                safe_name = original_name.replace(' ', '_').replace('/', '_')
                output_filename = f"{idx:02d}_{safe_name}.mp4"
                
                # Download video
                print(f"  Downloading as: {output_filename}")
                if self.download_video(video_info['url'], output_filename):
                    print(f"  ✓ Downloaded successfully")
                    self.downloaded_videos.append({
                        'query': query,
                        'original_name': original_name,
                        'filename': output_filename,
                        'timestamps': timestamps,
                        'video_info': video_info
                    })
                else:
                    print(f"  ✗ Download failed")
            else:
                print(f"  ✗ No suitable video found")
            
            # Rate limiting: wait between requests
            if idx < len(self.search_queries):
                time.sleep(2)  # Wait 2 seconds between requests
        
        return True
    
    def save_download_manifest(self):
        """Save manifest of downloaded videos."""
        print(f"\n[4/4] Saving download manifest...")
        
        manifest_path = self.output_dir / "download_manifest.json"
        
        manifest = {
            'total_videos': len(self.downloaded_videos),
            'source_pickle': str(self.pkl_file_path),
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'videos': self.downloaded_videos
        }
        
        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Manifest saved: {manifest_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error saving manifest: {e}")
            return False
    
    def run_full_pipeline(self):
        """Execute the complete download pipeline."""
        print("=" * 70)
        print("Pexels Complementary Video Downloader")
        print("=" * 70)
        
        # Load timestamp data
        if not self.load_pickle_data():
            return False
        
        # Generate search queries with Gemini
        if not self.generate_search_queries_with_gemini():
            return False
        
        # Download all videos
        if not self.download_all_videos():
            return False
        
        # Save manifest
        self.save_download_manifest()
        
        # Summary
        print("\n" + "=" * 70)
        print("✓ Pipeline completed successfully!")
        print("=" * 70)
        print(f"\nSummary:")
        print(f"  - Total videos downloaded: {len(self.downloaded_videos)}")
        print(f"  - Output directory: {self.output_dir.absolute()}")
        print(f"  - Manifest file: {self.output_dir / 'download_manifest.json'}")
        
        if self.downloaded_videos:
            print(f"\nDownloaded videos:")
            for video in self.downloaded_videos:
                print(f"  ✓ {video['filename']}")
                print(f"    Query: \"{video['query']}\"")
                print(f"    Timestamps: {video['timestamps'][0]} → {video['timestamps'][1]}")
        
        return True


def main():
    """Main entry point for the script."""
    print("\n" + "=" * 70)
    print("Pexels Complementary Video Downloader")
    print("=" * 70 + "\n")
    
    # Get API keys from environment variables
    pexels_api_key = os.getenv('PEXELS_API_KEY')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    if not pexels_api_key:
        print("Error: PEXELS_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export PEXELS_API_KEY='your-pexels-api-key'")
        print("\nGet your API key at: https://www.pexels.com/api/")
        sys.exit(1)
    
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        print("\nPlease set it using:")
        print("  export GEMINI_API_KEY='your-gemini-api-key'")
        sys.exit(1)
    
    # Get pickle file path
    if len(sys.argv) < 2:
        print("Usage: python download_complementary_videos.py PKL_FILE_PATH")
        print("\nExample:")
        print("  python download_complementary_videos.py data_sets/video_20241115_143022_timestamps.pkl")
        sys.exit(1)
    
    pkl_file_path = sys.argv[1]
    
    # Run the downloader
    downloader = PexelsVideoDownloader(pexels_api_key, gemini_api_key, pkl_file_path)
    success = downloader.run_full_pipeline()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
