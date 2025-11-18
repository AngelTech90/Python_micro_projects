# Video Integration Script with FFmpeg

Automatically integrate complementary videos into your main video at AI-analyzed timestamps. This is the final script (Part 3) of the video enhancement workflow.

## Overview

This tool completes the video enhancement pipeline by:

1. **Loading timestamp data** from the pickle file generated in Script 1
2. **Extracting video files** from the complementary videos directory (downloaded in Script 2)
3. **Using Gemini AI** to match and sort videos with timestamp keys for correct order
4. **Extracting durations** of all complementary videos using FFmpeg
5. **Calculating ideal durations** with Gemini AI based on required timestamps
6. **Trimming videos** to fit exact timestamp durations using FFmpeg (permanent)
7. **Integrating everything** into the final enhanced video with FFmpeg complex filters

## Requirements

### System Requirements

- **Operating System**: Linux (Debian-based recommended), macOS, or Windows with WSL
- **Python**: 3.7 or higher
- **FFmpeg**: Required (with libx264 and aac codec support)
- **Disk Space**: At least 2x the size of your original video
- **RAM**: Minimum 4GB recommended for HD video processing

### Python Libraries

Install all dependencies from `requirements.txt`:

```
google-generativeai>=0.3.0
python-dotenv>=1.0.0
pathlib>=1.0.1
```

### API Keys Required

- **Google Gemini API Key** - For video matching and duration calculation

## Installation

### 1. Install System Dependencies

#### On Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install ffmpeg python3 python3-pip python3-venv
```

#### On macOS:
```bash
brew install ffmpeg python3
```

#### Verify FFmpeg Installation:
```bash
ffmpeg -version
# Should show version with libx264 and aac support
```

### 2. Setup Python Environment

```bash
# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key with .env File

#### Create .env file:
```bash
touch .env
```

#### Add your Gemini API key:
```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key at: https://makersuite.google.com/app/apikey

#### Add .env to .gitignore:
```bash
echo ".env" >> .gitignore
```

**IMPORTANT**: Never commit your `.env` file to Git!

## Usage

### Basic Command

```bash
python integrate_complementary_videos.py ORIGINAL_VIDEO PKL_FILE COMPLEMENTARY_DIR
```

### Example

```bash
python integrate_complementary_videos.py \
    my_original_video.mp4 \
    data_sets/video_20241115_143022_timestamps.pkl \
    complementary_videos/
```

### Full Workflow Example

```bash
# Complete workflow from start to finish:

# Step 1: Analyze video and extract timestamps
python extract_and_analyze_timestamps.py my_video.mp4

# Step 2: Download complementary videos from Pexels
python download_complementary_videos.py data_sets/my_video_20241115_143022_timestamps.pkl

# Step 3: Integrate everything (THIS SCRIPT)
python integrate_complementary_videos.py \
    my_video.mp4 \
    data_sets/my_video_20241115_143022_timestamps.pkl \
    complementary_videos/

# Final output will be in:
# final_output/final_video_20241115_165500.mp4
```

## Expected Output

```
======================================================================
Video Integration Pipeline - FFmpeg + Gemini AI
======================================================================

✓ FFmpeg is installed and accessible

[1/7] Loading timestamp data from: data_sets/video_20241115_143022_timestamps.pkl
✓ Loaded 9 timestamp entries

Timestamp entries:
  1. smartphone_unboxing: 00:00:45 → 00:01:15
  2. design_showcase_360: 00:02:30 → 00:02:50
  3. display_quality_demo: 00:04:10 → 00:04:35
  4. camera_sample_photos: 00:06:20 → 00:06:55
  5. performance_benchmark_graphics: 00:08:15 → 00:08:40
  6. battery_test_visualization: 00:10:05 → 00:10:30
  7. comparison_competitor_phone: 00:11:45 → 00:12:10
  8. software_features_demo: 00:13:20 → 00:13:50
  9. price_value_infographic: 00:14:30 → 00:14:55

[2/7] Extracting video files from: complementary_videos
✓ Found 9 video files

Video files:
  1. 01_smartphone_unboxing.mp4
  2. 02_design_showcase_360.mp4
  3. 03_display_quality_demo.mp4
  4. 04_camera_sample_photos.mp4
  5. 05_performance_benchmark_graphics.mp4
  6. 06_battery_test_visualization.mp4
  7. 07_comparison_competitor_phone.mp4
  8. 08_software_features_demo.mp4
  9. 09_price_value_infographic.mp4

[3/7] Matching videos with timestamps using Gemini AI...
✓ Received response from Gemini AI
✓ Successfully sorted 9 videos

Sorted video order:
  1. smartphone_unboxing → 01_smartphone_unboxing.mp4
  2. design_showcase_360 → 02_design_showcase_360.mp4
  3. display_quality_demo → 03_display_quality_demo.mp4
  4. camera_sample_photos → 04_camera_sample_photos.mp4
  5. performance_benchmark_graphics → 05_performance_benchmark_graphics.mp4
  6. battery_test_visualization → 06_battery_test_visualization.mp4
  7. comparison_competitor_phone → 07_comparison_competitor_phone.mp4
  8. software_features_demo → 08_software_features_demo.mp4
  9. price_value_infographic → 09_price_value_infographic.mp4

[4/7] Extracting video durations with FFmpeg...
  1. 01_smartphone_unboxing.mp4: 35.50s
  2. 02_design_showcase_360.mp4: 20.00s
  3. 03_display_quality_demo.mp4: 28.75s
  4. 04_camera_sample_photos.mp4: 42.00s
  5. 05_performance_benchmark_graphics.mp4: 30.50s
  6. 06_battery_test_visualization.mp4: 28.00s
  7. 07_comparison_competitor_phone.mp4: 32.50s
  8. 08_software_features_demo.mp4: 35.25s
  9. 09_price_value_infographic.mp4: 27.00s
✓ Extracted durations for all 9 videos

[5/7] Calculating ideal durations with Gemini AI...
✓ Received response from Gemini AI
✓ Successfully calculated ideal durations

Duration adjustments:
  1. 01_smartphone_unboxing.mp4: 35.50s → 30.00s (CUT)
  2. 02_design_showcase_360.mp4: 20.00s (NO CHANGE)
  3. 03_display_quality_demo.mp4: 28.75s → 25.00s (CUT)
  4. 04_camera_sample_photos.mp4: 42.00s → 35.00s (CUT)
  5. 05_performance_benchmark_graphics.mp4: 30.50s → 25.00s (CUT)
  6. 06_battery_test_visualization.mp4: 28.00s → 25.00s (CUT)
  7. 07_comparison_competitor_phone.mp4: 32.50s → 25.00s (CUT)
  8. 08_software_features_demo.mp4: 35.25s → 30.00s (CUT)
  9. 09_price_value_infographic.mp4: 27.00s → 25.00s (CUT)

[6/7] Trimming videos to ideal durations with FFmpeg...
  1. 01_smartphone_unboxing.mp4: Trimming to 30.00s...
    ✓ Trimmed successfully
  2. 02_design_showcase_360.mp4: No trimming needed
  3. 03_display_quality_demo.mp4: Trimming to 25.00s...
    ✓ Trimmed successfully
  4. 04_camera_sample_photos.mp4: Trimming to 35.00s...
    ✓ Trimmed successfully
  5. 05_performance_benchmark_graphics.mp4: Trimming to 25.00s...
    ✓ Trimmed successfully
  6. 06_battery_test_visualization.mp4: Trimming to 25.00s...
    ✓ Trimmed successfully
  7. 07_comparison_competitor_phone.mp4: Trimming to 25.00s...
    ✓ Trimmed successfully
  8. 08_software_features_demo.mp4: Trimming to 30.00s...
    ✓ Trimmed successfully
  9. 09_price_value_infographic.mp4: Trimming to 25.00s...
    ✓ Trimmed successfully
✓ All videos trimmed successfully

[7/7] Integrating complementary videos into main video...
  Building FFmpeg filter chain...
  Executing FFmpeg integration (this may take several minutes)...
✓ Video integration completed successfully!
  Output: final_output/final_video_20241115_165500.mp4
  Size: 145.32 MB

======================================================================
✓ Pipeline completed successfully!
======================================================================
```

## Output

The script creates a `final_output/` directory with your enhanced video:

```
final_output/
└── final_video_20241115_165500.mp4
```

### Output Specifications

- **Format**: MP4 (H.264 video, AAC audio)
- **Video Codec**: libx264 (preset: medium, CRF: 23)
- **Audio Codec**: AAC (192 kbps)
- **Resolution**: Matches original video (complementary videos are scaled to fit)
- **Filename**: `final_video_{timestamp}.mp4`

## How It Works

### 7-Step Integration Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Load Timestamp Data                                 │
│   - Read .pkl file from Script 1                            │
│   - Extract timestamp keys and time ranges                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Extract Video Files                                 │
│   - Scan complementary_videos/ directory                    │
│   - List all .mp4 files                                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Sort Videos with Gemini AI                          │
│   - Match video filenames to timestamp keys                 │
│   - Return sorted list in correct order                     │
│   - Ensures proper integration sequence                     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Extract Video Durations (FFprobe)                   │
│   - Get actual duration of each complementary video         │
│   - Store durations in same order as sorted videos          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Calculate Ideal Durations (Gemini AI)               │
│   - Compare video durations with required timestamp ranges  │
│   - Determine which videos need trimming                    │
│   - Return ideal duration for each video                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Trim Videos (FFmpeg)                                │
│   - Cut videos to ideal durations                           │
│   - Overwrite original files permanently (no backup)        │
│   - Maintain high video quality                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 7: Integrate Videos (FFmpeg Complex Filter)            │
│   - Scale complementary videos to match original resolution │
│   - Overlay videos at specified timestamps                  │
│   - Merge audio from original video                         │
│   - Export final enhanced video                             │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Process Breakdown

#### Step 1: Load Timestamp Data

Reads the `.pkl` file generated by Script 1:

```python
{
    'smartphone_unboxing': ('00:00:45', '00:01:15'),     # 30 seconds needed
    'design_showcase_360': ('00:02:30', '00:02:50'),     # 20 seconds needed
    'display_quality_demo': ('00:04:10', '00:04:35'),    # 25 seconds needed
    # ... more entries
}
```

#### Step 2: Extract Video Files

Scans `complementary_videos/` directory:

```python
[
    '01_smartphone_unboxing.mp4',
    '02_design_showcase_360.mp4',
    '03_display_quality_demo.mp4',
    # ... more files
]
```

#### Step 3: Sort Videos with Gemini AI

**Why?** Video files may not be in the same order as timestamp keys. Gemini ensures correct matching.

**Gemini Prompt:**
```
You have a list of video filenames and timestamp keys.
Match each video filename with its corresponding timestamp key.
Return a sorted list of filenames in the order that matches timestamp keys.

Timestamp Keys: ["smartphone_unboxing", "design_showcase_360", ...]
Video Filenames: ["01_smartphone_unboxing.mp4", "02_design_showcase_360.mp4", ...]

Return ONLY a Python list of sorted video filenames.
```

**Gemini Output:**
```python
[
    "01_smartphone_unboxing.mp4",
    "02_design_showcase_360.mp4",
    "03_display_quality_demo.mp4",
    # ... correctly sorted
]
```

#### Step 4: Extract Video Durations

Uses FFprobe (part of FFmpeg) to get precise durations:

```bash
ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 video.mp4
```

**Result:**
```python
[35.5, 20.0, 28.75, 42.0, 30.5, ...]  # Actual durations in seconds
```

#### Step 5: Calculate Ideal Durations with Gemini AI

**Why?** Complementary videos might be longer than needed. Gemini calculates perfect durations to fit timestamps.

**Gemini Prompt:**
```
Compare video durations with required timestamp durations.
For videos longer than required, use the required duration.
For videos already fitting, keep original duration.

Data: [
    {
        "video": "01_smartphone_unboxing.mp4",
        "video_duration": 35.5,
        "required_duration": 30.0,
        "needs_cutting": true
    },
    # ... more comparisons
]

Return ONLY a Python list of ideal durations (float seconds).
```

**Gemini Output:**
```python
[30.0, 20.0, 25.0, 35.0, 25.0, ...]  # Ideal durations that fit timestamps
```

#### Step 6: Trim Videos with FFmpeg

For each video that needs trimming:

```bash
ffmpeg -i input.mp4 -t 30.0 -c:v libx264 -c:a aac -b:a 192k -y output.mp4
```

**Key parameters:**
- `-t 30.0`: Trim to 30 seconds
- `-c:v libx264`: Re-encode with H.264 (maintains quality)
- `-c:a aac`: Re-encode audio with AAC
- `-y`: Overwrite without confirmation

**Important:** This permanently modifies the video files in `complementary_videos/` directory. No backup is created.

#### Step 7: Integrate Videos with FFmpeg

Builds a complex FFmpeg filter to overlay all complementary videos at their specified timestamps:

```bash
ffmpeg \
  -i original_video.mp4 \
  -i 01_smartphone_unboxing.mp4 \
  -i 02_design_showcase_360.mp4 \
  -i 03_display_quality_demo.mp4 \
  -filter_complex "
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1];
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v2];
    [3:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v3];
    [0:v][v1]overlay=0:0:enable='between(t,45,75)'[tmp1];
    [tmp1][v2]overlay=0:0:enable='between(t,150,170)'[tmp2];
    [tmp2][v3]overlay=0:0:enable='between(t,250,275)'[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  final_output/final_video.mp4
```

**Filter breakdown:**
1. **Scale & Pad**: Resize each complementary video to match original resolution (1920x1080)
2. **Overlay**: Place each video at its specific timestamp using `enable='between(t,start,end)'`
3. **Chain**: Connect all overlays sequentially
4. **Audio**: Keep original video's audio track

## Gemini AI Integration Details

### First Gemini Call: Video Matching & Sorting

**Purpose:** Ensures complementary videos are integrated in the correct order matching timestamp keys.

**Input Data:**
- List of timestamp keys from `.pkl` file (e.g., `["smartphone_unboxing", "design_showcase_360", ...]`)
- List of video filenames from directory (e.g., `["01_smartphone_unboxing.mp4", "02_design_showcase_360.mp4", ...]`)

**AI Task:** Match and sort video filenames to correspond with timestamp key order.

**Output:** Sorted list of video filenames in the exact order needed for integration.

**Example:**
```python
# Input
timestamp_keys = ["smartphone_unboxing", "camera_sample_photos", "design_showcase_360"]
video_files = ["02_design_showcase_360.mp4", "01_smartphone_unboxing.mp4", "03_camera_sample_photos.mp4"]

# Gemini Output
sorted_videos = ["01_smartphone_unboxing.mp4", "03_camera_sample_photos.mp4", "02_design_showcase_360.mp4"]
```

---

### Second Gemini Call: Duration Optimization

**Purpose:** Calculate ideal durations for each video to fit perfectly within timestamp ranges.

**Input Data:**
- Current video durations (extracted by FFprobe)
- Required durations (calculated from timestamps: end_time - start_time)
- Comparison showing which videos need trimming

**AI Task:** Determine optimal duration for each video:
- If video is shorter/equal to required time: keep original duration
- If video is longer than required: use required duration for trimming

**Output:** List of ideal durations (float seconds) matching the video order.

**Example:**
```python
# Input
comparison_data = [
    {"video": "01_smartphone_unboxing.mp4", "video_duration": 35.5, "required_duration": 30.0},
    {"video": "02_design_showcase_360.mp4", "video_duration": 20.0, "required_duration": 20.0},
    {"video": "03_display_quality_demo.mp4", "video_duration": 28.75, "required_duration": 25.0}
]

# Gemini Output
ideal_durations = [30.0, 20.0, 25.0]  # First and third videos will be trimmed
```

## FFmpeg Operations Explained

### Operation 1: Extract Duration (ffprobe)

```bash
ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 video.mp4
```

**Purpose:** Get precise duration of complementary videos in seconds.

**Output:** Single number (e.g., `35.500000`)

---

### Operation 2: Trim Videos

```bash
ffmpeg -i input.mp4 -t 30.0 -c:v libx264 -c:a aac -b:a 192k -y temp_output.mp4
```

**Purpose:** Cut videos to exact required duration.

**Parameters:**
- `-i input.mp4`: Input file
- `-t 30.0`: Duration to keep (30 seconds)
- `-c:v libx264`: Video codec (H.264)
- `-c:a aac`: Audio codec
- `-b:a 192k`: Audio bitrate
- `-y`: Overwrite without asking
- `temp_output.mp4`: Temporary output (then replaces original)

**Note:** Original files are permanently overwritten (no backup created as per requirements).

---

### Operation 3: Video Integration (Complex Filter)

```bash
ffmpeg \
  -i original.mp4 \
  -i complementary1.mp4 \
  -i complementary2.mp4 \
  -filter_complex "
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1];
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,
         pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v2];
    [0:v][v1]overlay=0:0:enable='between(t,45,75)'[tmp1];
    [tmp1][v2]overlay=0:0:enable='between(t,150,170)'[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  output.mp4
```

**Filter Chain Breakdown:**

1. **Scale & Pad** (`scale=1920:1080:force_original_aspect_ratio=decrease,pad=...`):
   - Resizes complementary videos to match original resolution
   - Maintains aspect ratio
   - Adds padding if needed (centered)

2. **Overlay** (`overlay=0:0:enable='between(t,START,END)'`):
   - Places complementary video on top of original
   - `0:0` = position (top-left corner, full-screen replacement)
   - `enable='between(t,45,75)'` = only show between 45-75 seconds
   - Timestamp `t` is in seconds from video start

3. **Sequential Chaining** (`[0:v][v1]overlay...[tmp1]; [tmp1][v2]overlay...[tmp2]`):
   - Each overlay builds on the previous result
   - Allows multiple complementary videos at different timestamps

4. **Audio Mapping** (`-map "[out]" -map 0:a`):
   - Uses final processed video `[out]`
   - Keeps original video's audio track (`0:a`)

**Quality Settings:**
- `-preset medium`: Balance between encoding speed and file size
- `-crf 23`: Constant Rate Factor (lower = better quality, 18-28 is good range)
- `-b:a 192k`: Audio bitrate (192 kbps is high quality)

## Troubleshooting

### FFmpeg Not Found

**Error:** `✗ FFmpeg is not installed or not in PATH`

**Solution:**
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

---

### API Key Not Found

**Error:** `Error: GEMINI_API_KEY not found in .env file`

**Solution:**
```bash
# 1. Check if .env file exists
ls -la .env

# 2. If not, create it
touch .env

# 3. Add your API key
echo "GEMINI_API_KEY=your_actual_key_here" >> .env

# 4. Verify it's loaded
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

Get your API key at: https://makersuite.google.com/app/apikey

---

### File Not Found Errors

**Error:** `FileNotFoundError: Pickle file not found` or `Video not found`

**Solution:**
```bash
# Verify all required files exist
ls -la my_original_video.mp4
ls -la data_sets/*.pkl
ls -la complementary_videos/*.mp4

# Use absolute paths if needed
python integrate_complementary_videos.py \
    /full/path/to/video.mp4 \
    /full/path/to/timestamps.pkl \
    /full/path/to/complementary_videos/
```

---

### Video Count Mismatch

**Error:** `Expected X videos, got Y videos`

**Cause:** Number of video files doesn't match number of timestamp entries.

**Solution:**
```bash
# Check counts
python3 << EOF
import pickle
with open('data_sets/timestamps.pkl', 'rb') as f:
    data = pickle.load(f)
    print(f"Timestamp entries: {len(data)}")
EOF

ls complementary_videos/*.mp4 | wc -l  # Count video files

# Numbers should match!
```

If they don't match:
- Re-run Script 2 (download) to get all videos
- Check if some downloads failed
- Verify all videos downloaded successfully

---

### Gemini AI Sorting Failed

**Error:** `✗ Failed to sort videos properly`

**Possible Causes:**
1. Video filenames don't match timestamp key patterns
2. Gemini API returned unexpected format

**Solution:**
```bash
# Check video naming
ls -la complementary_videos/

# Videos should be named like: 01_key_name.mp4, 02_key_name.mp4

# If needed, manually verify in the script output which videos don't match
```

---

### Video Trimming Failed

**Error:** `✗ Trimming failed` during Step 6

**Possible Causes:**
1. Corrupted video file
2. Insufficient disk space
3. FFmpeg codec issues

**Solutions:**

**1. Test video integrity:**
```bash
ffmpeg -i complementary_videos/problematic_video.mp4 -f null -
# Should complete without errors
```

**2. Check disk space:**
```bash
df -h .
# Need at least 2x original video size
```

**3. Check video properties:**
```bash
ffprobe complementary_videos/problematic_video.mp4
# Look for codec, resolution, duration
```

**4. Try manual trim:**
```bash
ffmpeg -i complementary_videos/video.mp4 -t 30 -c:v libx264 -c:a aac test_output.mp4
```

---

### Video Integration Failed

**Error:** `✗ Video integration failed` during Step 7

**Common Causes:**
1. Not enough disk space
2. Out of memory
3. Complex filter chain error
4. Codec incompatibility

**Solutions:**

**1. Check disk space:**
```bash
df -h .
# Need space for full output video
```

**2. Check FFmpeg error output:**
The script shows the last 2000 characters of error output. Look for specific FFmpeg errors.

**3. Test with fewer videos:**
Edit the `.pkl` file to include only 2-3 timestamp entries and try again.

**4. Lower quality settings:**
Edit the script and change:
```python
"-preset", "fast",  # Instead of "medium"
"-crf", "28",  # Instead of "23" (lower quality, smaller file)
```

**5. Check memory usage:**
```bash
# While script runs, in another terminal:
watch -n 2 free -h

# If using too much memory, close other applications
```

---

### Out of Memory Errors

**Error:** System freezes, crashes, or Python memory errors

**Solutions:**

**1. Increase swap space:**
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**2. Process in batches:**
Split your complementary videos into smaller groups and integrate separately.

**3. Use faster preset:**
```python
# In script, change:
"-preset", "veryfast",  # Much faster, less memory
```

**4. Close other applications:**
Free up RAM by closing browsers, IDEs, etc.

---

### Audio Sync Issues

**Problem:** Audio is out of sync in final video

**Solutions:**

**1. Check original video audio:**
```bash
ffprobe -v error -select_streams a:0 \
        -show_entries stream=codec_name,sample_rate \
        original_video.mp4
```

**2. Re-encode with audio sync:**
```bash
ffmpeg -i final_output/final_video.mp4 \
       -c:v copy -c:a aac -b:a 192k -async 1 \
       final_video_fixed.mp4
```

**3. Verify complementary videos:**
Some complementary videos might have audio tracks causing conflicts. Check with:
```bash
ffprobe complementary_videos/video.mp4 | grep Audio
```

---

### Timestamp Synchronization Issues

**Problem:** Complementary videos appear at wrong times

**Solutions:**

**1. Verify timestamp format in .pkl:**
```python
import pickle
with open('data_sets/timestamps.pkl', 'rb') as f:
    data = pickle.load(f)
    for key, (start, end) in data.items():
        print(f"{key}: {start} → {end}")
```

Timestamps should be in `HH:MM:SS` or `MM:SS` format.

**2. Check video sorting:**
Review the console output from Step 3 to ensure Gemini sorted videos correctly.

**3. Test with single video:**
Modify the `.pkl` file to include only one timestamp entry and verify it appears at the correct time.

**4. Manual timestamp verification:**
```bash
# Play
