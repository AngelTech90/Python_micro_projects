# TensorPix Video Enhancer

AI-powered video upscaling and enhancement using TensorPix API with optimized settings for high-quality output.

## Overview

This script uses TensorPix's cloud-based AI to upscale videos to 1080p @ 60fps with the "People" preset and advanced AI upscaling. Perfect for improving low-resolution videos, restoring old footage, or enhancing content with people/faces.

## Features

- 🎬 **Upscale to 1080p Full HD** - AI-powered resolution enhancement
- 🎭 **People Preset** - Optimized for faces and human subjects
- 🎞️ **60 FPS Output** - Smooth frame interpolation
- 🤖 **AI 2x Upscale 4** - Advanced upscaling model
- 📦 **Batch Processing** - Process multiple videos
- ⚡ **Cloud Processing** - No GPU required locally
- 🎨 **Automatic Enhancements** - Denoise, sharpen, color correction

## Fixed Enhancement Settings

This script uses optimized, fixed settings for best quality:

| Setting | Value | Description |
|---------|-------|-------------|
| **Resolution** | 1080p Full HD | Output: 1920x1080 pixels |
| **Preset** | People | Optimized for human faces/subjects |
| **Frame Rate** | 60 FPS | Smooth motion interpolation |
| **AI Model** | 2x Upscale 4 | Advanced upscaling algorithm |
| **Denoise** | Enabled | Reduces video noise/grain |
| **Sharpen** | Enabled | Enhances detail clarity |
| **Color Enhance** | Enabled | Improves color balance/saturation |

## Requirements

### System Requirements
- Python 3.7 or higher
- Internet connection (stable, for upload/download)
- TensorPix API key (paid service)

### Python Dependencies
```bash
pip install requests
```

Or use the provided requirements file:
```bash
pip install -r requirements.txt
```

### API Key Setup

1. **Get your API key:**
   - Visit [https://tensorpix.ai/](https://tensorpix.ai/)
   - Create an account
   - Subscribe to a plan (check pricing)
   - Generate your API key

2. **Set environment variable:**
   ```bash
   # Linux/Mac
   export TENSORPIX_API_KEY="your_api_key_here"
   
   # Make it permanent
   echo 'export TENSORPIX_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Installation

```bash
# 1. Ensure Python 3.7+ is installed
python3 --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export TENSORPIX_API_KEY="your_api_key_here"

# 4. Test installation
python tensorpix_enhancer.py --help
```

## Usage

### Basic Usage

**Single Video:**
```bash
python tensorpix_enhancer.py input.mp4 -o output.mp4
```

**Multiple Videos to Directory:**
```bash
python tensorpix_enhancer.py video1.mp4 video2.mp4 video3.mp4 -o enhanced_directory/
```

**Batch Process Directory:**
```bash
python tensorpix_enhancer.py *.mp4 -o enhanced/
```

### With API Key Argument

```bash
python tensorpix_enhancer.py input.mp4 -o output.mp4 --api-key YOUR_API_KEY
```

### Command-Line Arguments

```
positional arguments:
  input                 Input video file(s) to enhance

optional arguments:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output file or directory (required)
  --api-key API_KEY     TensorPix API key (or set TENSORPIX_API_KEY env variable)
```

## Python Module Usage

```python
from tensorpix_enhancer import TensorPixEnhancer

# Initialize with API key
enhancer = TensorPixEnhancer(api_key="your_api_key")

# Enhance single video
enhancer.enhance_video("input.mp4", "output.mp4")

# Batch process
enhancer.enhance_batch(
    input_files=["video1.mp4", "video2.mp4"],
    output_dir="enhanced_videos"
)
```

## Supported Formats

### Input Formats
- MP4 (.mp4)
- MOV (.mov)
- AVI (.avi)
- MKV (.mkv)
- WebM (.webm)
- FLV (.flv)

### Output Format
- MP4 (1920x1080 @ 60fps)

## Processing Time

⚠️ **IMPORTANT:** AI video enhancement is VERY SLOW but produces excellent results.

### Typical Processing Times
- **Short video (1 minute):** ~10-15 minutes
- **Medium video (10 minutes):** ~2-3 hours
- **Long video (1 hour):** ~10-20 hours

### Factors Affecting Speed
- Source video quality (lower quality = longer processing)
- Video length
- TensorPix server load
- Complexity of the content

**Recommendation:** Process videos overnight or during off-hours.

## Examples

### Example 1: Upscale Old Footage
```bash
python tensorpix_enhancer.py old_video_480p.mp4 -o restored_1080p.mp4
```

### Example 2: Enhance Multiple Videos
```bash
python tensorpix_enhancer.py clip1.mp4 clip2.mp4 clip3.mp4 -o enhanced/
```

### Example 3: Batch Process Directory
```bash
# Enhance all MP4 files in current directory
python tensorpix_enhancer.py *.mp4 -o enhanced_videos/
```

## Best Results

### Recommended Source Material
✅ **Good candidates for enhancement:**
- Resolution: 480p, 720p (upscaling to 1080p)
- Content: Videos with people, faces, interviews
- Lighting: Good to moderate lighting
- Motion: Steady to moderate motion
- Quality: Decent source material (not heavily compressed)

❌ **Poor candidates:**
- Extremely low quality (<360p)
- Heavily compressed videos
- Very shaky footage
- Pure abstract/animation content
- Music videos with extreme effects

### Expected Improvements
- **Resolution:** Upscaled to 1920x1080
- **Frame Rate:** Smoothed to 60fps
- **Noise:** Reduced grain and artifacts
- **Sharpness:** Enhanced detail clarity
- **Colors:** Improved saturation and balance

## Cost Considerations

### Pricing (Approximate)
TensorPix is a **paid service**:
- Free tier: Very limited (check current limits)
- Pay-per-use: ~$0.10-$0.50 per minute of video
- Subscription plans: Available (check tensorpix.ai)

### Cost-Saving Tips
1. **Test with short clips first** (< 1 minute)
2. **Use for important content only** (worth the cost)
3. **Batch process efficiently** (upload all, process overnight)
4. **Monitor your credits/quota**
5. **Consider source quality** (garbage in = expensive garbage out)

## Workflow Examples

### Workflow 1: Complete Video Enhancement
```bash
# 1. Separate video and audio
python separator.py original.mp4

# 2. Enhance audio
python adobe_enhancer.py audio/original.mp3 -o enhanced_audio.mp3

# 3. Enhance video (THIS TAKES HOURS!)
python tensorpix_enhancer.py videos/original.mp4 -o enhanced_video.mp4

# 4. Mix back together
python mixer.py enhanced_video.mp4 enhanced_audio.mp3 -o final.mp4
```

### Workflow 2: Batch Archive Restoration
```bash
# Process old video archive overnight
python tensorpix_enhancer.py archive_videos/*.mp4 -o restored/
```

### Workflow 3: Test Before Full Processing
```bash
# 1. Extract 30-second sample
ffmpeg -i full_video.mp4 -t 30 -c copy sample.mp4

# 2. Enhance sample to verify quality
python tensorpix_enhancer.py sample.mp4 -o sample_enhanced.mp4

# 3. If satisfied, process full video
python tensorpix_enhancer.py full_video.mp4 -o enhanced_full.mp4
```

## Troubleshooting

### Error: "TensorPix API key required"
**Solution:**
```bash
export TENSORPIX_API_KEY="your_api_key_here"
```

### Processing Takes Very Long
**This is normal!** AI video enhancement is computationally expensive:
- 1 minute video = 10-30 minutes processing
- Be patient or process overnight
- Check job status periodically
- Don't close your terminal/computer

### Enhancement Failed
**Possible causes:**
- Source video is corrupted
- Unsupported video format
- API credits exhausted
- Server error

**Solutions:**
1. Verify source video plays correctly
2. Check file format is supported
3. Verify API credits/quota on tensorpix.ai
4. Try re-uploading
5. Contact TensorPix support

### Out of Credits/Quota
**Solution:**
- Wait for monthly quota reset (free tier)
- Purchase more credits
- Upgrade to paid plan

### Upload Failed
**Possible causes:**
- File too large
- Slow/unstable internet connection
- Server temporarily down

**Solutions:**
1. Check internet connection stability
2. Compress video before upload if very large
3. Retry upload
4. Check TensorPix status page

## Performance Tips

1. **Test First:** Always test with short clips (30 seconds) before processing long videos
2. **Overnight Processing:** Schedule long videos for overnight processing
3. **Batch Wisely:** Group similar videos for batch processing
4. **Monitor Progress:** Check progress periodically (script shows %)
5. **Source Quality:** Better source = better results, faster processing

## Limitations

### Technical Limitations
- ✗ Very slow processing (10-30 min per video minute)
- ✗ Requires stable internet connection
- ✗ Paid service (costs money)
- ✗ Cannot fix extremely poor source quality
- ✗ Fixed settings (optimized for people)
- ✓ Excellent results for appropriate content

### Service Limitations
- API rate limits (check TensorPix docs)
- File size limits (typically < 1GB per file)
- Processing queue (may wait during peak times)

## Alternatives

If TensorPix doesn't meet your needs:

1. **Topaz Video AI** - Local processing, one-time cost (~$299)
2. **Runway ML** - Alternative cloud service
3. **Real-ESRGAN** - Free, local, requires GPU
4. **FFmpeg** - Basic upscaling, no AI, free

## Modifying Settings

The script uses fixed optimal settings. To customize, modify `ENHANCEMENT_SETTINGS` in the code:

```python
ENHANCEMENT_SETTINGS = {
    "upscale": "4k",          # Change resolution
    "preset": "general",      # Change preset  
    "framerate": 30,          # Change FPS
    "ai_upscale": "2x_2"     # Change AI model
}
```

Available options:
- **Resolution:** 720p, 1080p, 4k
- **Preset:** people, general, anime, nature
- **Frame Rate:** 24, 30, 60
- **AI Model:** 2x_2, 2x_4, 4x_2, 4x_4

## Support & Resources

- **TensorPix Website:** [https://tensorpix.ai/](https://tensorpix.ai/)
- **API Documentation:** Check TensorPix developer docs
- **Script Help:** `python tensorpix_enhancer.py --help`
- **Pricing:** Check tensorpix.ai for current rates

## Version

Current Version: 1.0.0

Video Enhancement Pipeline Project

---

**Important:** AI enhancement takes time. Be patient and process overnight for best workflow!
