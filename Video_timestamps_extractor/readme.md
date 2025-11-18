# Video Timestamp Analyzer with Gemini AI

Automated video transcription extraction and AI-powered timestamp analysis for identifying optimal complementary video insertion points.

## Overview

This tool analyzes video transcriptions using Google's Gemini AI to automatically identify timestamps where complementary B-roll footage or supplementary video clips would enhance the content. Perfect for video editors looking to automate the process of finding insertion points for contextual footage.

### What it does

1. **Extracts transcription** from video files using FFmpeg (subtitle tracks or manual input)
2. **Analyzes content** with Gemini AI to identify up to 11 key moments where complementary videos would be beneficial
3. **Outputs structured timestamps** in both Python pickle (.pkl) and JSON formats for further processing

## Requirements

### System Requirements

- **Operating System**: Linux (Debian-based distributions recommended), also compatible with other Unix-like systems
- **Python**: 3.7 or higher
- **FFmpeg**: Required for video processing

### Python Libraries

All Python dependencies are listed in `requirements.txt`:

```
google-generativeai>=0.3.0
pathlib>=1.0.1
```

## Installation

### 1. Install System Dependencies

#### On Debian/Ubuntu:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv ffmpeg
```

#### On other systems:
- **macOS**: `brew install ffmpeg`
- **Arch Linux**: `sudo pacman -S ffmpeg`

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/video-timestamp-analyzer.git
cd video-timestamp-analyzer
```

### 3. Set Up Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

You need a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

#### Option A: Set as Environment Variable (Recommended)
```bash
export GEMINI_API_KEY='your-api-key-here'
```

To make it permanent, add to your `~/.bashrc` or `~/.zshrc`:
```bash
echo "export GEMINI_API_KEY='your-api-key-here'" >> ~/.bashrc
source ~/.bashrc
```

#### Option B: Pass as Command Line Argument
```bash
python extract_and_analyze_timestamps.py YOUR_API_KEY video.mp4
```

## Usage

### Basic Usage

```bash
python extract_and_analyze_timestamps.py path/to/your/video.mp4
```

### With API Key as Argument

```bash
python extract_and_analyze_timestamps.py YOUR_API_KEY path/to/your/video.mp4
```

### Example

```bash
# Using environment variable
python extract_and_analyze_timestamps.py my_tutorial_video.mp4

# Using command line argument
python extract_and_analyze_timestamps.py AIzaSyD... my_tutorial_video.mp4
```

## Output

The script creates two directories:

### `transcriptions/`
Contains extracted video transcriptions in text format:
- Filename: `{video_name}_{timestamp}.txt`
- Format: Timestamped text lines `[HH:MM:SS] transcription text`

### `data_sets/`
Contains analyzed timestamp data in two formats:

1. **Pickle file** (`.pkl`): Binary Python data structure for programmatic use
2. **JSON file** (`.json`): Human-readable format for inspection

#### Output Format

```python
{
    "car_model_showcase": ("00:02:15", "00:02:30"),
    "engine_details": ("00:05:42", "00:05:58"),
    "interior_features": ("00:08:20", "00:08:35"),
    # ... up to 11 entries
}
```

Each entry contains:
- **Key**: Descriptive name of the complementary video needed
- **Value**: Tuple with (start_timestamp, end_timestamp) in `HH:MM:SS` or `MM:SS` format

## Workflow Integration

This tool is designed to be part of a three-script workflow:

1. **This Script**: Extract transcription and analyze for timestamp insertion points
2. **Download Script** (to be created): Automatically search and download complementary videos based on the generated dictionary
3. **Integration Script** (to be created): Use FFmpeg to insert downloaded clips at specified timestamps into the original video

## Transcription Notes

### Automatic Extraction

The script attempts to extract embedded subtitle tracks from video files. If your video contains subtitles (SRT, VTT, etc.), they will be automatically extracted and formatted.

### Manual Transcription

If no subtitles are found, the script creates a template file. You should replace the placeholder with actual transcription content including timestamps before running the analysis.

**Recommended transcription tools:**
- [Whisper by OpenAI](https://github.com/openai/whisper) - Free, open-source, highly accurate
- YouTube auto-generated captions (if applicable)
- Manual transcription with timestamps

**Required format:**
```
[00:00:15] Introduction to the topic
[00:01:23] Discussing the main features
[00:03:45] Example demonstration
```

## Gemini AI Prompt

The script uses the following prompt to analyze transcriptions:

> "Use this video transcription as reference to find the time stamps in video that can be convenient to add a clip with some video that complements information of that part of video. If I'm talking about a car model, get the start time stamp and end time stamp to add a short video that complements what I'm talking about. Do this for max 11 parts of my video, then return only and absolutely nothing more than a dictionary in Python with adapted time stamps to then be processed with FFMPEG for adding specific videos."

The AI identifies contextual moments where additional footage would enhance viewer understanding or engagement.

## Troubleshooting

### FFmpeg Not Found

**Error**: `FFmpeg is not installed or not in PATH`

**Solution**: 
```bash
sudo apt-get install ffmpeg
# Verify installation
ffmpeg -version
```

### API Key Issues

**Error**: `GEMINI_API_KEY environment variable not set`

**Solutions**:
1. Set the environment variable: `export GEMINI_API_KEY='your-key'`
2. Pass as argument: `python script.py YOUR_KEY video.mp4`
3. Check your key at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution**:
```bash
pip install -r requirements.txt
```

Make sure your virtual environment is activated if you're using one.

### Video File Not Found

**Error**: `FileNotFoundError: Video file not found`

**Solution**: 
- Check the file path is correct
- Use absolute path: `/home/user/videos/my_video.mp4`
- Ensure you have read permissions for the file

### Permission Denied

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Make directories writable
chmod +w transcriptions/ data_sets/

# Or run with appropriate permissions
sudo python extract_and_analyze_timestamps.py video.mp4
```

## Advanced Configuration

### Customizing Output Directories

Edit the script's `__init__` method to change output directories:

```python
self.transcription_dir = Path("my_custom_transcriptions")
self.dataset_dir = Path("my_custom_datasets")
```

### Modifying the AI Prompt

To change how Gemini analyzes timestamps, edit the `prompt` variable in the `analyze_with_gemini` method.

### Changing Gemini Model

To use a different Gemini model, modify:

```python
self.model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Change model name here
```

Available models: `gemini-pro`, `gemini-2.0-flash-exp`, etc.

## Project Structure

```
video-timestamp-analyzer/
├── extract_and_analyze_timestamps.py  # Main script
├── requirements.txt                    # Python dependencies
├── README.md                          # This file
├── transcriptions/                    # Generated transcription files
└── data_sets/                         # Generated timestamp data
    ├── *.pkl                          # Pickle format
    └── *.json                         # JSON format
```

## API Rate Limits

Google Gemini API has rate limits depending on your tier:
- **Free tier**: 60 requests per minute
- **Paid tier**: Higher limits based on your plan

If you encounter rate limit errors, wait a few seconds and retry.

## Contributing

Contributions are welcome! This project is open-source and community-driven.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Provide detailed error messages and system information when reporting bugs

## Acknowledgments

- Google Gemini AI for powerful content analysis
- FFmpeg for video processing capabilities
- The open-source community for inspiration and tools

## Disclaimer

This tool is designed for legitimate video editing purposes. Users are responsible for:
- Complying with copyright laws when downloading and using complementary videos
- Ensuring proper licensing for all video content
- Following Google's Gemini API Terms of Service
- Respecting content creators' rights

---

**Made with ❤️ for video editors and content creators**
