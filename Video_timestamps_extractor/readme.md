# Video Timestamp Analyzer with AssemblyAI and Gemini AI

Automatically extract transcriptions from audio files and analyze them with AI to identify optimal timestamps for complementary video insertion. This is Part 1 of the video enhancement workflow.

## Overview

This tool:

1. **Extracts transcription** from audio using AssemblyAI API
2. **Analyzes content** with Gemini AI to identify up to 11 key moments for complementary videos
3. **Outputs structured timestamps** in Python pickle (.pkl) and JSON formats for further processing

## Requirements

### System Requirements

- **Operating System**: Linux (Debian-based recommended), macOS, or Windows
- **Python**: 3.7 or higher
- **Internet connection**: Required for API calls

### Python Libraries

All dependencies are listed in `requirements.txt`:

```
google-generativeai>=0.3.0
requests>=2.31.0
python-dotenv>=1.0.0
pathlib>=1.0.1
```

### API Keys Required

1. **Google Gemini API Key** - For content analysis
2. **AssemblyAI API Key** - For speech-to-text transcription

## Installation

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Get API Keys

#### Gemini API Key:
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

#### AssemblyAI API Key:
1. Visit [AssemblyAI Dashboard](https://www.assemblyai.com/app/api-keys)
2. Sign up or log in to your account
3. Copy your API key from the dashboard

### 3. Configure API Keys with .env File

#### Create .env file:
```bash
touch .env
```

#### Add your API keys:
```bash
# .env file
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
```

Get your keys from:
- **Gemini**: https://makersuite.google.com/app/apikey
- **AssemblyAI**: https://www.assemblyai.com/app/api-keys

#### Add .env to .gitignore:
```bash
echo ".env" >> .gitignore
```

**IMPORTANT**: Never commit your `.env` file to Git!

## Usage

### Basic Command

```bash
python extract_and_analyze_timestamps.py AUDIO_URL
```

### Example

```bash
# Analyze audio file from URL
python extract_and_analyze_timestamps.py https://example.com/audio.mp3
```

### Expected Output

```
============================================================
Video Timestamp Analyzer
============================================================

[1/3] Extracting transcription from audio using AssemblyAI API
  Submitting audio for transcription...
  ✓ Transcription submitted (ID: abc-123-def)
  Waiting for transcription to complete...
  Status: processing... (waiting 1/120)
  Status: processing... (waiting 2/120)
  ✓ Transcription completed
✓ Transcription extracted successfully
  Saved to: transcriptions/transcription_20241115_143022.txt

[2/3] Analyzing transcription with Gemini AI...
✓ Received response from Gemini AI
✓ Successfully parsed 9 timestamp entries

[3/3] Saving results to pickle file...
✓ Data saved successfully
  Saved to: data_sets/transcription_20241115_143022_timestamps.pkl
  JSON copy: data_sets/transcription_20241115_143022_timestamps.json

============================================================
✓ Pipeline completed successfully!
============================================================

Output files:
  - Transcription: transcriptions/transcription_20241115_143022.txt
  - Timestamps:    data_sets/transcription_20241115_143022_timestamps.pkl
  - JSON:          data_sets/transcription_20241115_143022_timestamps.json
```

## Output

The script creates two directories:

### `transcriptions/`
Contains extracted audio transcriptions in text format:
- Filename: `transcription_{timestamp}.txt`
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
- **Value**: Tuple with (start_timestamp, end_timestamp) in `HH:MM:SS` format

## How It Works

### 3-Step Pipeline

```
┌─────────────────────────────────────────────────┐
│ Step 1: Extract Transcription (AssemblyAI)      │
│   - Submit audio URL to AssemblyAI API          │
│   - Poll until transcription is complete        │
│   - Format with timestamps                      │
│   - Save to .txt file                           │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ Step 2: Analyze with Gemini AI                  │
│   - Send transcription to Gemini                │
│   - AI identifies insertion points              │
│   - Returns dictionary of timestamps            │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│ Step 3: Save Results                            │
│   - Save to .pkl file (binary format)           │
│   - Save to .json file (human-readable)         │
│   - Ready for next scripts                      │
└─────────────────────────────────────────────────┘
```

### Step 1: Extract Transcription with AssemblyAI

The script:
1. Submits your audio URL to AssemblyAI API
2. Polls the API every 5 seconds until transcription completes
3. Formats transcription with timestamps in `[HH:MM:SS] text` format
4. Saves to `transcriptions/transcription_{timestamp}.txt`

**AssemblyAI Features:**
- Supports multiple audio formats (.mp3, .wav, .m4a, etc.)
- Accurate speech-to-text with timestamps
- Up to 120 retries (10 minutes of waiting)

### Step 2: Analyze with Gemini AI

**Gemini Prompt:**
```
Use this video transcription as reference to find the time stamps 
in video that can be convenient to add a clip with some video that 
complements information of that part of video. If I'm talking about 
a car model, get the start time stamp and end time stamp to add a 
short video that complements what I'm talking about. Do this for 
max 11 parts of my video.

Return ONLY a Python dictionary with timestamps.
```

**What Gemini does:**
- Analyzes transcription content
- Identifies contextual moments for video insertion
- Returns up to 11 optimal timestamps
- Creates descriptive keys for each insertion point

### Step 3: Save Results

Two output files created:
1. **`.pkl` file**: Python pickle format for programmatic use
2. **`.json` file**: Human-readable JSON format

Both contain identical timestamp dictionaries.

## Workflow Integration

This is **Part 1 (First)** of the three-script video enhancement workflow:

### Complete Pipeline

```
┌────────────────────────────────────────────────────┐
│ PART 1: Timestamp Analysis (THIS SCRIPT)           │
│ Script: extract_and_analyze_timestamps.py          │
│                                                    │
│ INPUT:  Audio URL (https://example.com/audio.mp3) │
│ OUTPUT: data_sets/transcription_timestamps.pkl    │
│         transcriptions/transcription.txt           │
└────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────┐
│ PART 2: Download Complementary Videos             │
│ Script: download_complementary_videos.py          │
│                                                    │
│ INPUT:  Timestamps .pkl file                      │
│ OUTPUT: complementary_videos/*.mp4                │
└────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────┐
│ PART 3: Video Integration                         │
│ Script: integrate_complementary_videos.py         │
│                                                    │
│ INPUT:  Original video + complementary videos    │
│ OUTPUT: final_output/final_video.mp4              │
└────────────────────────────────────────────────────┘
```

## Troubleshooting

### API Key Not Found

**Error**: `GEMINI_API_KEY not found in .env file`

**Solution**:
```bash
# Create .env file
touch .env

# Add your API keys
echo "GEMINI_API_KEY=your_key" >> .env
echo "ASSEMBLYAI_API_KEY=your_key" >> .env

# Verify
cat .env
```

---

### AssemblyAI Transcription Fails

**Error**: `Transcription failed: Download error`

**Causes & Solutions**:
1. **Invalid audio URL**: Ensure URL is publicly accessible
2. **Unsupported format**: AssemblyAI supports: MP3, WAV, M4A, OGG, FLAC, ULAW
3. **Network issue**: Check your internet connection
4. **API key invalid**: Verify key at https://www.assemblyai.com/app/api-keys

---

### Transcription Timeout

**Error**: `Transcription timeout`

**Solution**:
- Large audio files may take longer than 10 minutes
- Edit `extract_transcription()` method and increase `max_retries`:
  ```python
  max_retries = 240  # 20 minutes instead of 10
  ```

---

### Gemini AI Parsing Failed

**Error**: `Failed to parse valid dictionary from response`

**Solution**:
- Transcription might be too short or unclear
- Try with clearer audio
- Check console output for Gemini's raw response

---

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'google.generativeai'`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
pip list | grep google-generativeai
```

---

### Permission Error

**Error**: `PermissionError: [Errno 13] Permission denied`

**Solution**:
```bash
# Make directories writable
chmod +w transcriptions/ data_sets/

# Or create if missing
mkdir -p transcriptions/ data_sets/
```

---

## Best Practices

### 1. Audio Quality

- Use clear, high-quality audio
- Minimum 160ms duration
- Remove background noise for better accuracy

### 2. API Key Security

- ✅ Use `.env` file with `python-dotenv`
- ✅ Add `.env` to `.gitignore`
- ✅ Never commit API keys to Git
- ✅ Rotate keys periodically

### 3. Testing

- Test with short audio files first (< 1 minute)
- Verify output files are created
- Check JSON format is valid

### 4. Storage Management

- Each transcription output: ~1-10 KB
- Each dataset file: ~1-5 KB
- Keep old files or delete periodically

## Advanced Usage

### Use with .env.example

Create a safe template for team:

```bash
# .env.example (safe to commit)
GEMINI_API_KEY=your_gemini_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_key_here
```

Team members copy:
```bash
cp .env.example .env
# Then edit .env with their actual keys
```

### Custom Output Directories

Edit the script's `__init__` method:

```python
self.transcription_dir = Path("my_transcriptions")
self.dataset_dir = Path("my_datasets")
```

### Change Gemini Model

Modify in `__init__`:

```python
self.model = genai.GenerativeModel('gemini-pro')  # Different model
```

Available: `gemini-pro`, `gemini-2.0-flash-exp`, etc.

## Credits

- **AssemblyAI**: For accurate speech-to-text transcription
- **Google Gemini AI**: For intelligent timestamp analysis
- **Open Source Community**: For inspiration and tools

## Support

For issues or questions:
- Check the Troubleshooting section above
- Visit [AssemblyAI Documentation](https://www.assemblyai.com/docs)
- Visit [Gemini API Docs](https://ai.google.dev/docs)
- Open an issue on GitHub

---

**Part 1 of Video Enhancement Toolkit**

Next: Download Complementary Videos (Script 2) → Video Integration (Script 3)
