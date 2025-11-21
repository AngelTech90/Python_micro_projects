# Adobe Audio Enhancer

AI-powered audio enhancement for single or multiple MP3 files using Adobe Podcast API.

## Overview

This script uses Adobe's cloud-based AI to enhance audio quality by removing background noise, normalizing volume levels, and improving speech clarity. Perfect for podcasts, interviews, voiceovers, and any speech content.

## Features

- 🎵 **Single File Enhancement** - Process one MP3 at a time
- 📦 **Batch Processing** - Process multiple MP3 files to a directory
- 🔇 **AI Noise Reduction** - Remove background noise intelligently
- 📊 **Automatic Normalization** - Consistent volume levels
- ⚡ **Cloud Processing** - No GPU or powerful hardware needed
- 🎙️ **Speech Optimized** - Best results for voice content

## Requirements

### System Requirements
- Python 3.7 or higher
- Internet connection
- Adobe Podcast API key

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
   - Visit [https://podcast.adobe.com/](https://podcast.adobe.com/)
   - Create a free account
   - Navigate to API settings
   - Generate your API key

2. **Set environment variable:**
   ```bash
   # Linux/Mac
   export ADOBE_API_KEY="your_api_key_here"
   
   # Make it permanent (add to ~/.bashrc or ~/.zshrc)
   echo 'export ADOBE_API_KEY="your_api_key_here"' >> ~/.bashrc
   source ~/.bashrc
   ```

## Installation

```bash
# 1. Ensure Python 3.7+ is installed
python3 --version

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
export ADOBE_API_KEY="your_api_key_here"

# 4. Test installation
python adobe_enhancer.py --help
```

## Usage

### Basic Usage

**Single File:**
```bash
python adobe_enhancer.py input.mp3 -o output.mp3
```

**Multiple Files to Directory:**
```bash
python adobe_enhancer.py file1.mp3 file2.mp3 file3.mp3 -o enhanced_directory/
```

**Batch Process All MP3s in Directory:**
```bash
python adobe_enhancer.py *.mp3 -o enhanced/
```

### With API Key Argument

If you don't want to set the environment variable:
```bash
python adobe_enhancer.py input.mp3 -o output.mp3 --api-key YOUR_API_KEY
```

### Command-Line Arguments

```
positional arguments:
  input                 Input MP3 file(s) to enhance

optional arguments:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output file or directory (required)
  --api-key API_KEY     Adobe API key (or set ADOBE_API_KEY env variable)
```

## Python Module Usage

You can also import and use this as a Python module:

```python
from adobe_enhancer import AdobeAudioEnhancer

# Initialize with API key
enhancer = AdobeAudioEnhancer(api_key="your_api_key")

# Enhance single file
enhancer.enhance_file("input.mp3", "output.mp3")

# Batch process multiple files
enhancer.enhance_batch(
    input_files=["file1.mp3", "file2.mp3", "file3.mp3"],
    output_dir="enhanced_audio"
)
```

## Examples

### Example 1: Enhance Podcast Episode
```bash
python adobe_enhancer.py raw_podcast.mp3 -o clean_podcast.mp3
```

### Example 2: Process Multiple Interviews
```bash
python adobe_enhancer.py interview1.mp3 interview2.mp3 interview3.mp3 -o cleaned_interviews/
```

### Example 3: Batch Process Directory
```bash
# Process all MP3s in current directory
python adobe_enhancer.py *.mp3 -o enhanced/
```

## Processing Details

### What Gets Enhanced
- **Noise Reduction:** AI removes background noise, hum, echo
- **Normalization:** Volume levels standardized to broadcast standards
- **Clarity:** Speech becomes clearer and more intelligible
- **Dynamics:** Compression and limiting applied automatically

### Processing Time
- **Typical:** 1-3 minutes per minute of audio
- **Upload time:** Depends on your internet connection
- **Processing:** Done on Adobe's servers
- **Download time:** Fast (compressed MP3)

### Output Format
- **Format:** MP3 (high quality)
- **Sample Rate:** 44.1kHz or 48kHz (preserved from source)
- **Bitrate:** High quality (~256-320kbps)
- **Channels:** Stereo or mono (preserved from source)

## Limitations

### Free Tier Limits
- **Processing Time:** Typically 30-60 minutes per month
- **File Size:** Up to ~500MB per file
- **File Duration:** Up to 2 hours per file
- **Format:** MP3 only

*Note: Check Adobe's current free tier limits as they may change*

### Technical Limitations
- ✗ Input must be MP3 format (convert other formats first)
- ✗ Requires internet connection
- ✗ Processing can take several minutes
- ✗ Optimized for speech (not ideal for music)
- ✗ Cannot recover completely destroyed audio
- ✓ Works best with decent source material

## Troubleshooting

### Error: "Adobe API key required"
**Solution:** Set your API key
```bash
export ADOBE_API_KEY="your_api_key_here"
```

### Error: "Only MP3 files supported"
**Solution:** Convert your audio to MP3 first
```bash
# Using ffmpeg
ffmpeg -i input.wav output.mp3
ffmpeg -i input.m4a output.mp3
```

### Error: "Upload failed"
**Possible causes:**
- No internet connection
- File too large (>500MB)
- API quota exceeded
- Invalid API key

**Solution:**
1. Check your internet connection
2. Verify file size: `ls -lh yourfile.mp3`
3. Check API quota on Adobe's website
4. Verify API key is correct

### Processing Takes Too Long
**Normal processing time:** 1-3 minutes per minute of audio
- Be patient, AI processing is not instant
- Check your internet connection
- For very long files (>1 hour), expect 1-3 hours processing

### Enhancement Quality Not Good
**Tips for better results:**
- Source should be at least decent quality (not extremely compressed)
- Works best for speech/voice content
- Music or highly compressed sources may not improve much
- Try re-recording with better microphone if possible

## Best Practices

1. **Input Quality:** Start with the best quality source you have
2. **File Format:** Convert to MP3 before processing (if not already)
3. **Backup Originals:** Always keep original files
4. **Test First:** Try with a short clip before processing long files
5. **Batch Processing:** Process multiple files at once to save time
6. **Monitor Quota:** Keep track of your monthly usage

## Workflow Examples

### Workflow 1: Podcast Production
```bash
# 1. Record podcast
# 2. Export as MP3
# 3. Enhance
python adobe_enhancer.py raw_episode.mp3 -o clean_episode.mp3
# 4. Edit/publish
```

### Workflow 2: Interview Cleanup
```bash
# Process multiple interview recordings
python adobe_enhancer.py interview*.mp3 -o cleaned/
```

### Workflow 3: Video Audio Enhancement
```bash
# 1. Extract audio from video
python separator.py video.mp4  # Creates audio/video.mp3

# 2. Enhance audio
python adobe_enhancer.py audio/video.mp3 -o enhanced.mp3

# 3. Mix back with video
python mixer.py videos/video.mp4 enhanced.mp3 -o final.mp4
```

## API Costs

### Free Tier (Typical)
- 30-60 minutes of processing per month
- Perfect for occasional use
- No credit card required

### Paid Plans
- Check [https://podcast.adobe.com/](https://podcast.adobe.com/) for current pricing
- Pay-as-you-go or subscription options
- Suitable for professional/commercial use

## Alternative Solutions

If Adobe doesn't meet your needs:

1. **Dolby.io API** - 50 hours/month free tier
2. **Auphonic** - Automated audio post-production
3. **Descript** - Audio editing with transcription
4. **FFmpeg** - Local processing (no AI, but free and unlimited)

## Support & Resources

- **Adobe Podcast:** [https://podcast.adobe.com/](https://podcast.adobe.com/)
- **API Documentation:** Check Adobe's developer portal
- **Script Help:** `python adobe_enhancer.py --help`

## Version

Current Version: 1.0.0

Video Enhancement Pipeline Project

---

**Need Help?** Run `python adobe_enhancer.py --help` for quick reference.
