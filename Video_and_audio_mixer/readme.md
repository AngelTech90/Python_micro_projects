# Video/Audio Mixer

Mix separate video and audio files into a single MP4 file using FFmpeg with two powerful modes: replace or mix.

## Overview

This script combines video and audio streams into a single file. It offers two modes: completely replace the video's audio, or mix new audio with the original audio track. Perfect for voiceovers, background music, audio enhancement workflows, and more.

## Features

- 🎬 **Replace Mode** - Replace video's audio completely with new audio
- 🎵 **Mix Mode** - Blend new audio with video's original audio
- 🔊 **Volume Control** - Adjust volume levels for both audio tracks
- ⚡ **Fast Processing** - No video re-encoding (5-20 seconds)
- 📦 **Batch Mode** - Auto-match and process multiple files
- 🎯 **Multiple Codecs** - AAC, MP3, FLAC, or copy original
- 💎 **No Video Quality Loss** - Video stream copied without processing

## Requirements

### System Requirements
- Python 3.7 or higher
- FFmpeg installed (required)

### Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora/RHEL
sudo dnf install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### Python Dependencies
No additional Python packages required! Uses only standard library.

## Installation

```bash
# 1. Ensure Python 3.7+ is installed
python3 --version

# 2. Install FFmpeg (see above)

# 3. Test the script
python mixer.py --help
```

## Mixing Modes

### Replace Mode (Default)
**What it does:** Completely replaces the video's audio with new audio

**Use cases:**
- Voice replacement/dubbing
- Adding new soundtrack
- Replacing poor quality audio with enhanced version
- Multilingual versions

**Command:**
```bash
python mixer.py video.mp4 audio.mp3 -o output.mp4
```

### Mix Mode
**What it does:** Blends new audio with video's original audio

**Use cases:**
- Adding background music
- Adding sound effects
- Adding narration while keeping original audio
- Mixing music with dialogue

**Command:**
```bash
python mixer.py video.mp4 music.mp3 -o output.mp4 --mode mix
```

## Usage

### Basic Usage

**Replace Audio (Default):**
```bash
python mixer.py video.mp4 audio.mp3 -o output.mp4
```

**Mix Audio with Original:**
```bash
python mixer.py video.mp4 music.mp3 -o output.mp4 --mode mix
```

**Custom Volume Levels (Mix Mode):**
```bash
python mixer.py video.mp4 music.mp3 -o output.mp4 --mode mix \
    --new-volume 0.8 --original-volume 0.5
```

**High Quality Audio:**
```bash
# AAC with higher bitrate
python mixer.py video.mp4 audio.wav -o output.mp4 --audio-bitrate 512k

# Lossless FLAC
python mixer.py video.mp4 audio.wav -o output.mp4 --audio-codec flac
```

**Batch Mode (Auto-Match Files):**
```bash
python mixer.py --batch \
    --video-dir videos/ \
    --audio-dir audio/ \
    -o mixed/
```

### Command-Line Arguments

```
# Single file mode
positional arguments:
  video                      Input video file
  audio                      Input audio file
  -o, --output OUTPUT        Output file (required)

optional arguments:
  -h, --help                 Show help message
  --mode MODE                Mixing mode: replace (default) or mix
  --audio-codec CODEC        Audio codec: aac (default), mp3, flac, copy
  --audio-bitrate RATE       Audio bitrate (default: 320k)
  --new-volume VOL           New audio volume for mix mode (default: 1.0)
  --original-volume VOL      Original audio volume for mix mode (default: 0.3)

# Batch mode
  --batch                    Enable batch processing
  --video-dir DIR            Video directory for batch mode
  --audio-dir DIR            Audio directory for batch mode
```

## Python Module Usage

```python
from mixer import MediaMixer

mixer = MediaMixer()

# Replace mode
mixer.mix_file(
    video_file="video.mp4",
    audio_file="audio.mp3",
    output_file="output.mp4",
    mode="replace"
)

# Mix mode with custom volumes
mixer.mix_file(
    video_file="video.mp4",
    audio_file="music.mp3",
    output_file="output.mp4",
    mode="mix",
    new_volume=0.8,
    original_volume=0.5
)

# Batch processing
pairs = [
    ("video1.mp4", "audio1.mp3"),
    ("video2.mp4", "audio2.mp3")
]

results = mixer.mix_batch(
    video_audio_pairs=pairs,
    output_dir="mixed",
    mode="replace"
)
```

## Volume Control (Mix Mode)

### Volume Range
- **0.0** = Muted (silent)
- **0.5** = Half volume
- **1.0** = Full volume (original level)
- **1.5+** = Amplified (may cause distortion/clipping)

### Recommended Settings

**Background Music (music quieter):**
```bash
--new-volume 0.4 --original-volume 1.0
```

**Voice Over (original quieter):**
```bash
--new-volume 1.0 --original-volume 0.2
```

**Equal Mix:**
```bash
--new-volume 1.0 --original-volume 1.0
```

**Subtle Background:**
```bash
--new-volume 0.3 --original-volume 1.0
```

⚠️ **Important:** Keep total volume under ~1.5 to avoid audio clipping and distortion.

## Supported Formats

### Input Formats
- **Video:** MP4, MKV, AVI, MOV, WebM, FLV, WMV, etc.
- **Audio:** MP3, WAV, AAC, M4A, FLAC, OGG, etc.

### Output Format
- **MP4** (universal compatibility)

### Audio Codecs
| Codec | Quality | Size | Compatibility | Use Case |
|-------|---------|------|---------------|----------|
| **AAC** (default) | Excellent | Small | Universal | Best for most uses |
| **MP3** | Good | Small | Universal | Legacy compatibility |
| **FLAC** | Lossless | Large | Limited | Archival, editing |
| **Copy** | Original | Original | Varies | Fastest, no re-encoding |

## Performance

### Speed
- **Very Fast:** 5-20 seconds per file
- **No Video Re-encoding:** Video quality preserved
- **RAM Usage:** < 100MB

### Typical Processing Times
| Video Length | Processing Time |
|--------------|-----------------|
| 1 minute | ~5 seconds |
| 10 minutes | ~10 seconds |
| 1 hour | ~20 seconds |
| 2 hours | ~30 seconds |

*Times may vary based on disk speed and audio encoding settings*

## Examples

### Example 1: Voice Replacement
```bash
# Separate original
python separator.py interview.mp4

# Enhance audio
python adobe_enhancer.py audio/interview.mp3 -o enhanced.mp3

# Mix back
python mixer.py videos/interview.mp4 enhanced.mp3 -o final.mp4
```

### Example 2: Add Background Music
```bash
python mixer.py video.mp4 music.mp3 -o with_music.mp4 --mode mix \
    --new-volume 0.4 --original-volume 1.0
```

### Example 3: Multilingual Version
```bash
# Replace English audio with Spanish audio
python mixer.py video_english.mp4 audio_spanish.mp3 -o video_spanish.mp4
```

### Example 4: Batch Production
```bash
# Process multiple video-audio pairs
python mixer.py --batch \
    --video-dir videos/ \
    --audio-dir enhanced_audio/ \
    -o final/
```

## Batch Mode Details

### How It Works
Batch mode automatically matches files by name:

```
videos/clip1.mp4  +  audio/clip1.mp3  →  mixed/mixed_clip1.mp4
videos/clip2.mp4  +  audio/clip2.mp3  →  mixed/mixed_clip2.mp4
videos/clip3.mp4  +  audio/clip3.mp3  →  mixed/mixed_clip3.mp4
```

### Matching Logic
The script looks for audio files with the same base name:
1. First tries: `clip1.mp3`
2. Then tries: `clip1.wav`
3. Then tries: `clip1.m4a`

### Batch Command
```bash
python mixer.py --batch \
    --video-dir videos/ \
    --audio-dir audio/ \
    -o output_directory/
```

## Complete Workflow Examples

### Workflow 1: Audio Enhancement Pipeline
```bash
# 1. Separate video and audio
python separator.py original.mp4 --audio-format wav

# 2. Enhance audio with AI
python adobe_enhancer.py audio/original.wav -o enhanced.mp3

# 3. Mix enhanced audio back with video
python mixer.py videos/original.mp4 enhanced.mp3 -o final.mp4
```

### Workflow 2: Batch Audio Enhancement
```bash
# 1. Separate all videos
python separator.py *.mp4

# 2. Enhance all audio files
python adobe_enhancer.py audio/*.mp3 -o enhanced/

# 3. Mix back (batch mode)
python mixer.py --batch \
    --video-dir videos/ \
    --audio-dir enhanced/ \
    -o final/
```

### Workflow 3: Add Music to Multiple Videos
```bash
# Create audio directory with music files named to match videos
mkdir audio
cp background_music.mp3 audio/video1.mp3
cp background_music.mp3 audio/video2.mp3
cp background_music.mp3 audio/video3.mp3

# Batch mix
python mixer.py --batch \
    --video-dir videos/ \
    --audio-dir audio/ \
    -o with_music/ \
    --mode mix \
    --new-volume 0.3 \
    --original-volume 1.0
```

## Troubleshooting

### Error: "FFmpeg not found"
**Solution:** Install FFmpeg
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Verify
ffmpeg -version
```

### Error: "File not found"
**Solution:** Check file paths
```bash
# Use absolute paths
python mixer.py /full/path/to/video.mp4 /full/path/to/audio.mp3 -o output.mp4

# Or navigate to directory first
cd /path/to/files
python mixer.py video.mp4 audio.mp3 -o output.mp4
```

### Warning: Duration Mismatch
**What it means:** Video and audio have different lengths

**Behavior:** Output will be the length of the shortest stream
- 10s video + 12s audio = 10s output
- 12s video + 10s audio = 10s output

**Solution (if timing is critical):**
```bash
# Trim audio to match video length
ffmpeg -i audio.mp3 -t 00:01:30 -c copy audio_trimmed.mp3

# Or trim video to match audio
ffmpeg -i video.mp4 -t 00:01:30 -c copy video_trimmed.mp4
```

### Audio Out of Sync
**Possible causes:**
- Source files already out of sync
- Different frame rates
- Variable frame rate video

**Solution:**
1. Verify source files individually
2. Try different audio codec: `--audio-codec aac`
3. Check original video/audio sync before mixing
4. Re-export source video with constant frame rate

### No Audio in Output
**Possible causes:**
- Audio file has no audio stream
- Audio codec incompatible
- Wrong file type

**Solution:**
1. Verify audio file: `ffplay audio.mp3`
2. Check audio stream: `ffprobe audio.mp3`
3. Try different codec: `--audio-codec aac`
4. Re-export audio file

### Audio Quality Issues
**For better quality:**
```bash
# Higher bitrate
python mixer.py video.mp4 audio.mp3 -o output.mp4 --audio-bitrate 512k

# Lossless
python mixer.py video.mp4 audio.wav -o output.mp4 --audio-codec flac
```

## Duration Handling

The script uses FFmpeg's `-shortest` flag:
- Output ends when the shortest stream ends
- Warns if duration difference > 1 second
- Prevents partial audio or black video at end

**Example:**
- Video: 2 minutes 30 seconds
- Audio: 2 minutes 20 seconds
- **Output:** 2 minutes 20 seconds

## Quality Best Practices

### Audio Quality
**Standard Quality:**
```bash
--audio-codec aac --audio-bitrate 192k
```

**High Quality (default):**
```bash
--audio-codec aac --audio-bitrate 320k
```

**Professional/Archival:**
```bash
--audio-codec aac --audio-bitrate 512k
```

**Lossless:**
```bash
--audio-codec flac
```

### Video Quality
✅ **No quality loss** - Video is always copied without re-encoding
- Original codec preserved
- Original bitrate preserved  
- Original resolution preserved
- Fast processing (no video encoding time)

## Common Use Cases

### 1. Podcast/Interview Production
```bash
# Replace poor audio with studio-quality enhanced version
python mixer.py interview_video.mp4 enhanced_audio.mp3 -o final_podcast.mp4
```

### 2. YouTube Content Creation
```bash
# Add intro music mixed with voiceover
python mixer.py intro_video.mp4 intro_music.mp3 -o intro_final.mp4 --mode mix \
    --new-volume 0.5 --original-volume 1.0
```

### 3. Music Videos
```bash
# Add music track to video
python mixer.py footage.mp4 song.mp3 -o music_video.mp4
```

### 4. Multilingual Content
```bash
# Create different language versions
python mixer.py video.mp4 audio_spanish.mp3 -o video_spanish.mp4
python mixer.py video.mp4 audio_french.mp3 -o video_french.mp4
python mixer.py video.mp4 audio_german.mp3 -o video_german.mp4
```

### 5. Educational Videos
```bash
# Mix narration with background music
python mixer.py lesson_video.mp4 narration.mp3 -o lesson_final.mp4 --mode mix \
    --new-volume 1.0 --original-volume 0.3
```

### 6. Sound Design
```bash
# Add sound effects to video
python mixer.py scene.mp4 sound_effects.mp3 -o scene_with_sfx.mp4 --mode mix \
    --new-volume 0.7 --original-volume 1.0
```

## Tips & Best Practices

1. **Test First:** Always test with short clips before processing long videos
2. **Backup Originals:** Keep original files until you verify output
3. **Volume Levels:** Start conservative with mix mode (0.3-0.5 for background)
4. **Format:** Use AAC codec for best compatibility
5. **Batch Processing:** Name files consistently for automatic batch matching
6. **Quality Check:** Listen to output before sharing/publishing
7. **Sync Verification:** Verify audio is in sync throughout entire video

## Integration with Other Tools

This script works perfectly with the video enhancement pipeline:

```bash
# Complete pipeline example
# 1. Separate
python separator.py raw.mp4

# 2. Enhance audio
python adobe_enhancer.py audio/raw.mp3 -o enhanced_audio.mp3

# 3. Enhance video (optional, slow)
python tensorpix_enhancer.py videos/raw.mp4 -o enhanced_video.mp4

# 4. Mix back together
python mixer.py enhanced_video.mp4 enhanced_audio.mp3 -o final.mp4
```

## Limitations

- Cannot mix more than 2 audio tracks (video's audio + new audio)
- Batch mode requires matching file names
- Output format is always MP4 (most compatible)
- Mix mode requires video to have original audio

## Support & Resources

- **FFmpeg Documentation:** [https://ffmpeg.org/documentation.html](https://ffmpeg.org/documentation.html)
- **Script Help:** `python mixer.py --help`
- **FFmpeg Audio Filters:** [https://ffmpeg.org/ffmpeg-filters.html#Audio-Filters](https://ffmpeg.org/ffmpeg-filters.html#Audio-Filters)

## Version

Current Version: 1.0.0

Video Enhancement Pipeline Project

---

**Quick Start:** `python mixer.py video.mp4 audio.mp3 -o output.mp4` - That simple!
