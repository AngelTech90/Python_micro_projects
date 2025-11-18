# Pexels Complementary Video Downloader

Automatically search and download complementary stock videos from Pexels based on AI-analyzed timestamps. This script is part 2 of the video enhancement workflow.

## Overview

This tool takes the timestamp analysis data (`.pkl` file) from the first script and:

1. **Loads timestamp data** from the pickle file
2. **Uses Gemini AI** to generate optimized Pexels search queries
3. **Searches Pexels API** for suitable stock videos matching required durations
4. **Downloads videos** with proper naming and organization
5. **Creates a manifest** tracking all downloaded videos and their metadata

## Requirements

### System Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.7 or higher
- **Internet connection**: Required for API calls and video downloads

### Python Libraries

All dependencies are listed in `requirements.txt`:

```
google-generativeai>=0.3.0
requests>=2.31.0
pathlib>=1.0.1
```

### API Keys Required

1. **Pexels API Key** - Free tier available
2. **Google Gemini API Key** - For generating search queries

## Installation

### 1. Install Python Dependencies

```bash
# Activate your virtual environment (if using one)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Get Pexels API Key

1. Visit [Pexels API](https://www.pexels.com/api/)
2. Click "Get Started" or "Sign Up"
3. Create a free account
4. Generate your API key from the dashboard
5. Free tier includes: **200 requests per hour**

### 3. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 4. Configure API Keys

#### Set Environment Variables (Recommended)

```bash
# Pexels API Key
export PEXELS_API_KEY='your-pexels-api-key-here'

# Gemini API Key
export GEMINI_API_KEY='your-gemini-api-key-here'
```

#### Make Permanent (Optional)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo "export PEXELS_API_KEY='your-pexels-api-key'" >> ~/.bashrc
echo "export GEMINI_API_KEY='your-gemini-api-key'" >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Usage

```bash
python download_complementary_videos.py path/to/timestamps.pkl
```

### Example

```bash
# Using a timestamp file from the first script
python download_complementary_videos.py data_sets/smartphone_review_20241115_143022_timestamps.pkl
```

### Expected Output

```
======================================================================
Pexels Complementary Video Downloader
======================================================================

[1/4] Loading timestamp data from: data_sets/smartphone_review_20241115_143022_timestamps.pkl
✓ Loaded 9 timestamp entries

Timestamp entries:
  1. smartphone_unboxing: 00:00:45 → 00:01:15 (30s)
  2. design_showcase_360: 00:02:30 → 00:02:50 (20s)
  3. display_quality_demo: 00:04:10 → 00:04:35 (25s)
  ...

[2/4] Generating search queries with Gemini AI...
✓ Received response from Gemini AI
✓ Generated 9 search queries

Search queries:
  1. "smartphone unboxing"
  2. "phone design 360"
  3. "display screen test"
  ...

[3/4] Searching and downloading videos from Pexels...

[1/9] Processing: "smartphone unboxing"
  Original key: smartphone_unboxing
  Timestamp: 00:00:45 → 00:01:15
  Required duration: 30s
  Searching Pexels...
  ✓ Found video (ID: 3571264)
    Quality: 1920x1080
    Duration: 35s
  Downloading as: 01_smartphone_unboxing.mp4
  Downloading: 100.0%
  ✓ Downloaded successfully

[2/9] Processing: "phone design 360"
  ...

[4/4] Saving download manifest...
✓ Manifest saved: complementary_videos/download_manifest.json

======================================================================
✓ Pipeline completed successfully!
======================================================================

Summary:
  - Total videos downloaded: 9
  - Output directory: /home/user/project/complementary_videos
  - Manifest file: complementary_videos/download_manifest.json

Downloaded videos:
  ✓ 01_smartphone_unboxing.mp4
    Query: "smartphone unboxing"
    Timestamps: 00:00:45 → 00:01:15
  ✓ 02_design_showcase_360.mp4
    Query: "phone design 360"
    Timestamps: 00:02:30 → 00:02:50
  ...
```

## Output Structure

The script creates a `complementary_videos/` directory with:

### Downloaded Videos

Videos are named systematically:

```
complementary_videos/
├── 01_smartphone_unboxing.mp4
├── 02_design_showcase_360.mp4
├── 03_display_quality_demo.mp4
├── 04_camera_sample_photos.mp4
├── 05_performance_benchmark_graphics.mp4
├── 06_battery_test_visualization.mp4
├── 07_comparison_competitor_phone.mp4
├── 08_software_features_demo.mp4
├── 09_price_value_infographic.mp4
└── download_manifest.json
```

### Naming Convention

- **Format**: `{index:02d}_{original_key_name}.mp4`
- **Index**: Two-digit number (01, 02, 03...) matching order in timestamp file
- **Name**: Sanitized version of the original dictionary key from timestamps

### Download Manifest

The `download_manifest.json` file tracks all downloads:

```json
{
  "total_videos": 9,
  "source_pickle": "data_sets/smartphone_review_20241115_143022_timestamps.pkl",
  "download_date": "2024-11-15 14:35:22",
  "videos": [
    {
      "query": "smartphone unboxing",
      "original_name": "smartphone_unboxing",
      "filename": "01_smartphone_unboxing.mp4",
      "timestamps": ["00:00:45", "00:01:15"],
      "video_info": {
        "id": 3571264,
        "url": "https://player.vexels.com/video-files/...",
        "width": 1920,
        "height": 1080,
        "duration": 35,
        "quality": "hd"
      }
    },
    {
      "query": "phone design 360",
      "original_name": "design_showcase_360",
      "filename": "02_design_showcase_360.mp4",
      "timestamps": ["00:02:30", "00:02:50"],
      "video_info": {
        "id": 2873486,
        "url": "https://player.vexels.com/video-files/...",
        "width": 1920,
        "height": 1080,
        "duration": 25,
        "quality": "hd"
      }
    }
    // ... more entries
  ]
}
```

## How It Works

### Step-by-Step Process

#### 1. Load Timestamp Data

The script reads the `.pkl` file generated by the first script:

```python
# Example data loaded from pickle
timestamps = {
    'smartphone_unboxing': ('00:00:45', '00:01:15'),
    'design_showcase_360': ('00:02:30', '00:02:50'),
    'display_quality_demo': ('00:04:10', '00:04:35'),
    'camera_sample_photos': ('00:06:20', '00:06:55'),
    # ... more entries
}
```

#### 2. Generate Search Queries with Gemini AI

**Input to Gemini:**
```
Based on this dictionary of video timestamps and their descriptions, 
generate search queries for finding complementary stock videos on Pexels.

For each entry in the dictionary, create a clear, concise search query 
(2-4 words) that would find relevant stock footage on Pexels.

IMPORTANT: Return ONLY a Python list of search query strings, nothing else.

Example output format:
["smartphone unboxing", "phone design closeup", "display screen demo"]

Timestamp Data:
{
    "smartphone_unboxing": ["00:00:45", "00:01:15"],
    "design_showcase_360": ["00:02:30", "00:02:50"],
    ...
}
```

**Output from Gemini:**
```python
[
    "smartphone unboxing",
    "phone design 360 view",
    "display screen test",
    "camera lens macro shot",
    "phone performance test",
    "battery charging animation",
    "phone comparison chart",
    "mobile interface demo",
    "phone price tag"
]
```

#### 3. Search Pexels API

For each search query:
- Calculates required video duration from timestamps (end_time - start_time)
- Sends request to Pexels API with the query
- Retrieves up to 15 video results
- Filters results by minimum duration requirement
- Selects highest quality video (preferably HD: 1920x1080)
- Falls back to best available if no exact duration match

#### 4. Download Videos

- Downloads videos sequentially to avoid rate limits
- Shows real-time download progress (percentage)
- Renames files using systematic naming convention
- Saves to `complementary_videos/` directory
- Implements 2-second delay between downloads

#### 5. Create Download Manifest

- Records all download metadata in JSON format
- Includes original timestamps for reference
- Links downloaded videos to their intended purpose
- Stores Pexels video information (ID, quality, duration)
- Enables easy tracking for the next script

## Gemini AI Integration

### Purpose

Gemini AI analyzes the timestamp dictionary keys and generates optimized search queries for Pexels that will find the most relevant stock footage.

### Prompt Structure

The script sends this exact prompt to Gemini:

```
Use this video transcription as reference to find the time stamps in video 
that can be convenient to add a clip with some video that complements 
information of that part of video.

Based on this dictionary of video timestamps and their descriptions, 
generate search queries for finding complementary stock videos on Pexels.

For each entry in the dictionary, create a clear, concise search query 
(2-4 words) that would find relevant stock footage on Pexels.

IMPORTANT: Return ONLY a Python list of search query strings, nothing else. 
No explanation, no markdown, no code blocks. Just the raw Python list.

Example output format:
["smartphone unboxing", "phone design closeup", "display screen demo"]

Timestamp Data:
{timestamp_dictionary_here}

Generate the search queries now:
```

### Why Use Gemini?

1. **Context Understanding**: Interprets semantic meaning of timestamp keys
2. **Query Optimization**: Generates Pexels-specific search terms (2-4 words optimal)
3. **Flexibility**: Adapts to any video content type (tech, cooking, travel, education, etc.)
4. **Consistency**: Ensures search queries match the original video's context
5. **Intelligence**: Transforms technical keys like "battery_test_visualization" into searchable terms like "battery charging animation"

### Example Transformations

| Original Key | Gemini Generated Query |
|--------------|------------------------|
| `smartphone_unboxing` | "smartphone unboxing" |
| `engine_bay_closeup` | "car engine detail" |
| `stirring_technique_demonstration` | "cooking stirring technique" |
| `autopilot_demonstration` | "self driving car demo" |
| `parmesan_grating_shot` | "cheese grating closeup" |

## Pexels API Details

### Rate Limits

- **Free Tier**: 200 requests per hour
- **Per Month**: No hard limit on free tier
- **Rate Limiting Strategy**: Script includes 2-second delays between requests
- **Auto-Retry**: Automatically waits 60 seconds if rate limit is hit (429 error)

### Video Selection Logic

The script follows this priority order:

1. **Search** Pexels with query → Get up to 15 results
2. **Filter** by minimum duration (calculated from timestamps)
3. **Prefer HD quality** (1920x1080 or 1280x720)
4. **Select highest resolution** among filtered results
5. **Fallback** to first result if no duration match found
6. **Return** video download URL and metadata

### Video Quality Preferences

Priority order for video quality selection:

1. **Full HD** (1920x1080) - Preferred
2. **HD** (1280x720) - Acceptable
3. **SD** (854x480) - Fallback
4. **Any available** - Last resort

### Video Specifications

- **Format**: MP4 (H.264 codec)
- **Orientation**: Landscape (configurable)
- **Source**: Pexels free stock videos
- **License**: Pexels License (free for commercial use)

## Troubleshooting

### API Key Issues

**Error**: `Error: PEXELS_API_KEY environment variable not set`

**Solution**:
```bash
export PEXELS_API_KEY='your-pexels-api-key-here'
```

Get your free API key at: https://www.pexels.com/api/

**Verification**:
```bash
echo $PEXELS_API_KEY  # Should display your key
```

---

**Error**: `Error: GEMINI_API_KEY environment variable not set`

**Solution**:
```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

Get your key at: https://makersuite.google.com/app/apikey

---

### Rate Limit Errors

**Error**: `⚠ Rate limit reached, waiting 60 seconds...`

**What it means**: You've exceeded 200 requests per hour on Pexels free tier

**Solutions**:
1. **Wait**: Script automatically waits and retries
2. **Check usage**: Visit your Pexels dashboard to see current usage
3. **Upgrade**: Consider paid tier for higher limits (20,000+ requests/hour)
4. **Reduce load**: Process smaller batches of videos

**Prevention**:
- The script already includes 2-second delays between requests
- Don't modify the delay to be shorter
- Plan large downloads during off-peak hours

---

### No Videos Found

**Error**: `✗ No suitable video found`

**Causes**:
1. Search query too specific or unusual
2. No videos match the required duration
3. Temporary Pexels API issue

**Solutions**:

1. **Check the query**: Look at what Gemini generated
   ```bash
   # In output you'll see:
   Search queries:
     1. "very specific technical term"  # ← Too specific
   ```

2. **Manual override**: Edit search queries in the script
   ```python
   # After line with generate_search_queries_with_gemini()
   # Add manual override:
   self.search_queries[0] = "broader search term"
   ```

3. **Try broader terms**: 
   - Instead of: "tesla model 3 autopilot system"
   - Use: "self driving car"

4. **Check Pexels manually**: Search pexels.com to verify content exists

---

### Download Failures

**Error**: `✗ Download failed: 403` or `✗ Download error`

**Solutions**:

1. **Check internet connection**:
   ```bash
   ping pexels.com
   ```

2. **Verify disk space**:
   ```bash
   df -h .  # Check available space
   ```

3. **Check permissions**:
   ```bash
   ls -ld complementary_videos/
   chmod +w complementary_videos/  # Make writable
   ```

4. **Retry individual video**: Re-run the script (it will skip existing downloads)

5. **Check Pexels status**: Visit https://www.pexels.com/ to ensure service is operational

---

### Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'requests'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep requests
pip list | grep google-generativeai
```

---

**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution**:
```bash
pip install google-generativeai
# or
pip install -r requirements.txt
```

---

### Pickle File Errors

**Error**: `FileNotFoundError: Pickle file not found: data_sets/...`

**Solutions**:

1. **Verify file exists**:
   ```bash
   ls -la data_sets/*.pkl
   ```

2. **Check path**: Use correct path from first script output
   ```bash
   # First script outputs:
   # "Saved to: data_sets/video_20241115_143022_timestamps.pkl"
   # Use exact path:
   python download_complementary_videos.py data_sets/video_20241115_143022_timestamps.pkl
   ```

3. **Use absolute path**:
   ```bash
   python download_complementary_videos.py /full/path/to/data_sets/file.pkl
   ```

4. **Run from correct directory**: Make sure you're in the project root

---

**Error**: `Error loading pickle file: ...`

**Cause**: Corrupted or incompatible pickle file

**Solutions**:
1. Re-run the first script to regenerate the pickle file
2. Check the JSON version (same filename with `.json` extension)
3. Verify Python version compatibility

---

### Gemini AI Errors

**Error**: `✗ Error generating search queries: ...`

**Solutions**:

1. **Check API key validity**:
   ```bash
   # Test with a simple API call
   curl -H "Content-Type: application/json" \
        -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY"
   ```

2. **Verify quota**: Check your Gemini API dashboard for rate limits

3. **Check network**: Ensure you can reach Google APIs
   ```bash
   ping generativelanguage.googleapis.com
   ```

4. **Try different model**: Edit script to use `gemini-pro` instead of `gemini-2.0-flash-exp`

---

### Parse Errors

**Error**: `✗ Failed to parse search queries from response`

**Cause**: Gemini returned unexpected format

**Solutions**:

1. **Check raw response**: Script will display it automatically

2. **Manual extraction**: If you see the list in output, manually create it:
   ```python
   # In the script after generate_search_queries_with_gemini()
   self.search_queries = [
       "query 1",
       "query 2",
       # ... copy from output
   ]
   ```

3. **Update prompt**: Make the Gemini prompt more explicit about format

---

### Permission Errors

**Error**: `PermissionError: [Errno 13] Permission denied: 'complementary_videos'`

**Solutions**:

1. **Check directory permissions**:
   ```bash
   ls -ld complementary_videos/
   ```

2. **Fix permissions**:
   ```bash
   chmod +w complementary_videos/
   # or
   sudo chown $USER:$USER complementary_videos/
   ```

3. **Create directory manually**:
   ```bash
   mkdir -p complementary_videos
   chmod 755 complementary_videos
   ```

---

### Common Issues Summary

| Issue | Quick Fix |
|-------|-----------|
| Missing API key | `export PEXELS_API_KEY='your-key'` |
| Rate limit | Wait 60 seconds, script auto-retries |
| No videos found | Use broader search terms |
| Download fails | Check internet & disk space |
| Import error | `pip install -r requirements.txt` |
| File not found | Use absolute path to `.pkl` file |

## Workflow Integration

This is **Part 2** of a three-script workflow for automated video enhancement:

### Complete Workflow

```
┌─────────────────────────────────────────────────────────┐
│  Part 1: Extract & Analyze Timestamps                  │
│  Script: extract_and_analyze_timestamps.py             │
│  Input:  Video file (.mp4, .mkv, etc.)                 │
│  Output: timestamps.pkl + transcription.txt            │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Part 2: Download Complementary Videos (THIS SCRIPT)   │
│  Script: download_complementary_videos.py              │
│  Input:  timestamps.pkl                                │
│  Output: complementary_videos/*.mp4 + manifest.json    │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│  Part 3: Integrate Videos (Coming Soon)                │
│  Script: integrate_complementary_videos.py             │
│  Input:  original video + complementary_videos/        │
│  Output: final_enhanced_video.mp4                      │
└─────────────────────────────────────────────────────────┘
```

### Data Flow Between Scripts

#### From Script 1 → Script 2:

**Input**: `data_sets/video_20241115_143022_timestamps.pkl`

```python
{
    'smartphone_unboxing': ('00:00:45', '00:01:15'),
    'design_showcase_360': ('00:02:30', '00:02:50'),
    # ... more entries
}
```

#### From Script 2 → Script 3:

**Outputs**:
1. `complementary_videos/01_smartphone_unboxing.mp4`
2. `complementary_videos/02_design_showcase_360.mp4`
3. `complementary_videos/download_manifest.json`

**Manifest structure** (for Script 3 to use):
```json
{
  "videos": [
    {
      "filename": "01_smartphone_unboxing.mp4",
      "timestamps": ["00:00:45", "00:01:15"],
      "original_name": "smartphone_unboxing"
    }
  ]
}
```

### Using Output in Next Script

The third script will:
1. Read `download_manifest.json`
2. Load original video
3. Use FFmpeg to insert each complementary video at specified timestamps
4. Apply transitions/effects
5. Export final enhanced video

## Advanced Configuration

### Customizing Search Behavior

#### 1. Override Gemini Search Queries

If you want manual control over search queries:

```python
# Edit download_complementary_videos.py
# After line: if not self.generate_search_queries_with_gemini():

# Add this override:
self.search_queries = [
    "your custom query 1",
    "your custom query 2",
    "your custom query 3",
    # ... one per timestamp entry
]
```

#### 2. Change Video Orientation

```python
# In search_pexels_video() method, modify params:
params = {
    "query": query,
    "per_page": 15,
    "orientation": "portrait"  # Options: "landscape", "portrait", "square"
}
```

#### 3. Adjust Quality Preferences

Edit the quality selection logic in `search_pexels_video()`:

```python
# For maximum quality only (larger files):
if vf.get('width', 0) >= 1920:  # Full HD only
    hd_video = vf
    break

# For smaller files (SD quality):
if vf.get('width', 0) >= 854:  # SD quality
    hd_video = vf
    break

# For mobile-optimized:
if 720 <= vf.get('width', 0) <= 1280:  # 720p-1080p
    hd_video = vf
    break
```

#### 4. Modify Download Delay

Change rate limiting behavior:

```python
# In download_all_videos() method:

# More conservative (safer for rate limits):
time.sleep(5)  # Wait 5 seconds between requests

# Less delay (riskier, faster):
time.sleep(1)  # Wait 1 second (may hit rate limits)

# Variable delay based on file size:
delay = 2 if video_info['duration'] < 30 else 3
time.sleep(delay)
```

#### 5. Change Results Per Query

```python
# In search_pexels_video() method:
params = {
    "query": query,
    "per_page": 30,  # Get more results (max 80)
    "orientation": "landscape"
}
```

#### 6. Filter by Specific Duration Range

```python
# Add duration filtering:
for video in data['videos']:
    video_duration = video.get('duration', 0)
    
    # Only accept videos within 5 seconds of required duration
    if abs(video_duration - min_duration) <= 5:
        # Process this video
```

#### 7. Custom Output Directory

```python
# In __init__ method:
self.output_dir = Path("my_custom_videos")  # Change from "complementary_videos"
self.output_dir.mkdir(exist_ok=True)
```

#### 8. Change Naming Convention

```python
# In download_all_videos() method:
# Current: 01_smartphone_unboxing.mp4
# Custom options:

# Option A: No index prefix
output_filename = f"{safe_name}.mp4"

# Option B: Include video ID
output_filename = f"{idx:02d}_{video_info['id']}_{safe_name}.mp4"

# Option C: Include duration
output_filename = f"{idx:02d}_{safe_name}_{min_duration}s.mp4"
```

### Custom Gemini Model

```python
# In __init__ method:
self.model = genai.GenerativeModel('gemini-pro')  # Use different model
# Available: 'gemini-pro', 'gemini-2.0-flash-exp', 'gemini-pro-vision'
```

### Batch Processing Multiple Pickle Files

```bash
# Create a bash script: batch_download.sh
#!/bin/bash

for pkl_file in data_sets/*.pkl; do
    echo "Processing: $pkl_file"
    python download_complementary_videos.py "$pkl_file"
    sleep 10  # Wait between batches
done
```

## Best Practices

### 1. API Key Security

**DO:**
- ✅ Use environment variables for API keys
- ✅ Add `.env` files to `.gitignore`
- ✅ Rotate API keys periodically
- ✅ Use separate keys for development and production

**DON'T:**
- ❌ Hard-code API keys in scripts
- ❌ Commit API keys to Git repositories
- ❌ Share API keys in public forums
- ❌ Use production keys for testing

**Example secure setup**:
```bash
# .env file (add to .gitignore)
PEXELS_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Load in script with python-dotenv
pip install python-dotenv

# In script:
from dotenv import load_dotenv
load_dotenv()
```

### 2. Rate Limiting

**Strategy:**
- Keep default 2-second delay between requests
- Monitor Pexels dashboard for usage statistics
- Schedule large downloads during off-peak hours (night/early morning)
- Consider upgrading to paid tier for high-volume projects

**Monitoring usage:**
```python
# Add to script for tracking
total_requests = len(self.search_queries)
requests_per_hour = (3600 / 2)  # With 2-second delay
hours_needed = total_requests / requests_per_hour

print(f"Estimated time: {hours_needed:.1f} hours")
print(f"Total requests: {total_requests}")
```

### 3. Video Quality Management

**For best results:**
1. **Test first**: Download 1-2 videos to check quality before batch processing
2. **Review manifest**: Check `video_info` in JSON for actual downloaded quality
3. **Set standards**: Define minimum acceptable quality (e.g., 1280x720)
4. **Manual review**: Some automated selections may need replacement

**Quality checklist:**
```
✓ Resolution: Minimum 1280x720 (HD)
✓ Duration: Matches or exceeds required timestamp duration
✓ Content: Relevant to original video context
✓ Style: Consistent with overall video aesthetic
✓ Licensing: Pexels License confirmed
```

### 4. Storage Management

**Planning storage:**
- HD video (1920x1080): ~10-50MB per video
- 11 videos (max): ~110-550MB per project
- Include buffer: Plan for 1GB per project

**Disk space check:**
```bash
# Before running script
df -h .

# Check specific directory size
du -sh complementary_videos/

# Clean up old projects
rm -rf old_project/complementary_videos/
```

**Backup strategy:**
```bash
# Archive completed projects
tar -czf project_name_videos.tar.gz complementary_videos/

# Upload to cloud storage
rsync -av complementary_videos/ user@backup-server:/backups/
```

### 5. Search Query Optimization

**Tips for better results:**

1. **Review Gemini output**: Always check generated queries before proceeding
2. **Keep it simple**: 2-4 words work best on Pexels
3. **Use common terms**: Avoid technical jargon
4. **Test manually**: Search pexels.com first to verify content exists
5. **Iterate**: Re-run with adjusted queries if results are poor

**Good vs Bad queries:**

| ❌ Too Specific | ✅ Better Alternative |
|-----------------|----------------------|
| "iPhone 15 Pro Max unboxing" | "smartphone unboxing" |
| "Tesla Model 3 autonomous driving" | "self driving car" |
| "Canon EOS R5 manual focus" | "camera manual focus" |
| "Italian Arborio rice cooking" | "cooking rice" |

### 6. Error Handling

**Implement logging:**
```python
# Add to script
import logging

logging.basicConfig(
    filename='download_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Use throughout script
logging.info(f"Starting download for {query}")
logging.error(f"Download failed: {e}")
```

**Recovery strategy:**
- Script automatically skips existing files on re-run
- Check manifest to see what was completed
- Re-run script to continue from where it stopped

### 7. Content Verification

**Before using downloaded videos:**

1. **Preview each video**: Quick visual check
2. **Verify duration**: Ensure it matches needs
3. **Check relevance**: Does content match context?
4. **Test integration**: Insert one video to test workflow

**Automated verification script** (optional):
```python
import cv2

def verify_video(filepath):
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        return False
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps
    
    cap.release()
    return duration > 0

# Check all videos
for video_file in Path("complementary_videos").glob("*.
