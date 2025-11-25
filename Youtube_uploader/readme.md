# YouTube Video Auto-Uploader

A Python script to automatically upload videos to YouTube with custom metadata (title, description, tags, and thumbnail) using the YouTube Data API v3.

## Features

- 🎬 Automated video uploads to YouTube
- 📝 Custom titles from text files
- 📄 Detailed descriptions support
- 🏷️ Hashtags and tags automation
- 🖼️ Custom thumbnail uploads
- 🔄 Resumable uploads with retry logic
- 📊 Upload progress tracking
- ⚙️ Template-based metadata system
- 🎯 Multiple video format support
- 🔐 Secure OAuth 2.0 authentication

## Libraries Used

This script uses the following Python libraries:

### **google-auth** (v2.23.0+)
- **Purpose**: Core authentication library for Google APIs
- **Used in script**: 
  - `from google.auth.transport.requests import Request` - Refreshes expired OAuth tokens
  - `from google.oauth2.credentials import Credentials` - Manages OAuth 2.0 credentials
- **Why needed**: Handles the OAuth 2.0 authentication flow and manages access tokens for YouTube API access

### **google-auth-oauthlib** (v1.1.0+)
- **Purpose**: OAuth 2.0 integration for Google Auth Library
- **Used in script**:
  - `from google_auth_oauthlib.flow import InstalledAppFlow` - Runs the OAuth authorization flow
- **Why needed**: Provides the browser-based login flow on first run and creates initial credentials from your `client_secrets.json` file

### **google-auth-httplib2** (v0.1.1+)
- **Purpose**: HTTP transport adapter for Google Auth
- **Used in script**: Automatically used by `googleapiclient` behind the scenes
- **Why needed**: Enables authenticated HTTP requests to YouTube API with automatic token refresh

### **google-api-python-client** (v2.100.0+)
- **Purpose**: Official Google API client library
- **Used in script**:
  - `from googleapiclient.discovery import build` - Creates the YouTube API service instance
  - `from googleapiclient.http import MediaFileUpload` - Handles video and thumbnail uploads with resumable capability
  - `from googleapiclient.errors import HttpError` - Catches and handles API errors
- **Why needed**: Provides the main interface to interact with YouTube Data API (upload videos, set thumbnails, manage metadata)

### **Standard Python Libraries**
The script also uses built-in Python libraries:
- `os` - File system operations and path handling
- `json` - Reading/writing JSON files (credentials and tokens)
- `pathlib.Path` - Modern file path handling and directory traversal
- `time` - Sleep functionality for retry logic
- `random` - Random jitter for exponential backoff
- `http.client` & `httplib2` - HTTP connection handling and error management

## Prerequisites

- Python 3.7 or higher
- A Google account with a YouTube channel
- Google Cloud project with YouTube Data API v3 enabled
- **Verified YouTube channel** (required for custom thumbnails)

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/youtube-auto-uploader.git
   cd youtube-auto-uploader
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name and click "Create"

### Step 2: Enable YouTube Data API v3

1. In the Cloud Console, navigate to "APIs & Services" → "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - App name: "YouTube Auto Uploader" (or your choice)
   - User support email: Your email
   - Developer contact: Your email
   - **Scopes**: Add `https://www.googleapis.com/auth/youtube.upload`
   - Test users: Add your email
4. Select "Desktop app" as application type
5. Name it (e.g., "YouTube Uploader Desktop")
6. Click "Create"
7. Download the JSON file
8. **Rename it to `client_secrets.json`** and place it in the script directory

### Step 4: Verify Your YouTube Channel (For Custom Thumbnails)

Custom thumbnails require a verified YouTube account:

1. Go to [https://www.youtube.com/verify](https://www.youtube.com/verify)
2. Follow the verification process (phone verification)
3. Wait for verification confirmation

**Without verification**, the script will still upload videos successfully, but thumbnail uploads will fail with a 403 error.

## Video Package Structure

The script expects your video files organized in a folder with the following structure:

```
video_package/
├── video.mp4           # Your video file (required)
├── title.txt           # Video title (required)
├── description.txt     # Video description (optional)
├── tags.txt            # Tags/hashtags (optional)
└── thumbnail.png       # Custom thumbnail (optional)
```

### File Specifications

#### **video.mp4** (or other formats)
- **Supported formats**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`
- **Recommended**: H.264 codec, MP4 container
- **Maximum size**: YouTube allows up to 256GB or 12 hours

#### **title.txt**
- **Content**: Your video title
- **Character limit**: 100 characters (enforced by YouTube)
- **Example**:
  ```
  Amazing Python Tutorial - Beginner Friendly!
  ```

#### **description.txt**
- **Content**: Detailed video description
- **Character limit**: 5000 characters (enforced by YouTube)
- **Supports**: Line breaks, URLs, timestamps
- **Example**:
  ```
  In this tutorial, we'll learn Python basics.
  
  🔗 Resources:
  - GitHub: https://github.com/username/repo
  - Documentation: https://docs.python.org
  
  ⏱️ Timestamps:
  0:00 - Introduction
  2:30 - Setup
  5:00 - Coding
  ```

#### **tags.txt**
- **Content**: Comma-separated or space-separated tags
- **Character limit**: 500 characters total (enforced by YouTube)
- **Note**: Hashtags (#) are automatically removed from tags array
- **Examples**:
  ```
  # Comma-separated:
  python, programming, tutorial, coding, beginners
  
  # Space-separated:
  python programming tutorial coding beginners
  
  # With hashtags (# will be removed automatically):
  #python #programming #tutorial #coding #beginners
  ```

#### **thumbnail.png** (or .jpg)
- **Supported formats**: `.png`, `.jpg`, `.jpeg`
- **Recommended size**: 1280x720 pixels (16:9 aspect ratio)
- **Minimum size**: 640x360 pixels
- **Maximum file size**: 2MB
- **Image quality**: High resolution, clear text if any

## Configuration

Edit the `main()` function in `upload_to_youtube.py`:

```python
# Path to your video package folder
VIDEO_FOLDER = "./video_package"

# Privacy status: "public", "private", or "unlisted"
PRIVACY_STATUS = "private"

# Category ID (see list below)
CATEGORY_ID = "22"  # People & Blogs
```

### YouTube Category IDs

- `1` - Film & Animation
- `2` - Autos & Vehicles
- `10` - Music
- `15` - Pets & Animals
- `17` - Sports
- `19` - Travel & Events
- `20` - Gaming
- `22` - People & Blogs (default)
- `23` - Comedy
- `24` - Entertainment
- `25` - News & Politics
- `26` - Howto & Style
- `27` - Education
- `28` - Science & Technology

## Usage

### First Run

1. **Prepare your video package** following the structure above

2. **Run the script:**
   ```bash
   python upload_to_youtube.py
   ```

3. **Authenticate:**
   - Your browser will open automatically
   - Sign in to your Google account
   - You'll see "Google hasn't verified this app" warning - click **"Continue"**
   - Grant permissions to upload videos
   - The script will save authentication tokens

### Subsequent Runs

The script will use saved tokens and run without browser interaction:

```bash
python upload_to_youtube.py
```

## Upload Process

The script performs the following steps:

1. **Validation**: Checks if all required files exist
2. **Metadata Loading**: Reads title, description, and tags from text files
3. **Authentication**: Connects to YouTube API using OAuth 2.0
4. **Video Upload**: Uploads video with resumable upload (handles network interruptions)
5. **Thumbnail Upload**: Sets custom thumbnail (if provided and channel is verified)
6. **Confirmation**: Displays video ID and URL

## Important Notes

### Testing Mode vs. Published App

⚠️ **CRITICAL**: If your OAuth app is in "Testing" mode, all uploaded videos will be **locked as Private** and cannot be changed to Public/Unlisted.

**To upload Public/Unlisted videos:**

1. Go to Google Cloud Console → "OAuth consent screen"
2. Click "Publish App"
3. Submit for verification (if needed)

**OR for personal use:**

- Keep the app in Testing mode
- Upload as Private
- Manually change privacy in YouTube Studio after upload

### API Quotas

YouTube Data API has daily quota limits:

- **Daily quota**: 10,000 units
- **Video upload cost**: ~1600 units per video
- **Thumbnail upload cost**: ~50 units per thumbnail
- **Approximate uploads per day**: 6 videos

Quota resets at midnight Pacific Time (PT).

### Upload Time

Upload time depends on:
- Video file size
- Your internet upload speed
- YouTube processing time

**Example timings:**
- 100MB video: 2-5 minutes (on 50 Mbps upload)
- 500MB video: 10-20 minutes
- 2GB video: 30-60 minutes

The script shows upload progress percentage.

## Troubleshooting

### "client_secrets.json not found"
- Ensure you've downloaded OAuth credentials from Google Cloud Console
- Rename the file to exactly `client_secrets.json`
- Place it in the same directory as the script

### Videos stuck as "Private"
- Your OAuth app is in Testing mode
- Publish the app in Google Cloud Console, OR
- Manually change privacy in YouTube Studio after upload

### "403 Forbidden - Cannot upload custom thumbnails"
- Your YouTube channel is not verified
- Verify at [https://www.youtube.com/verify](https://www.youtube.com/verify)
- Videos will still upload without thumbnails

### "Quota exceeded" error
- You've reached the daily API quota limit (10,000 units)
- Wait until midnight Pacific Time for quota reset
- Consider spacing out uploads throughout the day

### Upload fails or times out
- Check your internet connection
- The script has automatic retry logic (up to 10 retries)
- Large files may take longer - be patient

### "Invalid grant" error
- Delete `youtube_token.json` and run the script again
- Re-authenticate when prompted

## Automation Ideas

### Schedule Daily Uploads (Linux/Mac - cron)

```bash
# Edit crontab
crontab -e

# Upload daily at 3 AM
0 3 * * * cd /path/to/youtube-auto-uploader && /usr/bin/python3 upload_to_youtube.py
```

### Schedule Daily Uploads (Windows - Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily at specific time)
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `C:\path\to\upload_to_youtube.py`
   - Start in: `C:\path\to\youtube-auto-uploader\`

### Batch Upload Multiple Videos

Create a batch script:

```python
import os
from upload_to_youtube import upload_video_package

video_folders = [
    "./video1",
    "./video2",
    "./video3",
]

for folder in video_folders:
    print(f"\nProcessing {folder}...")
    video_id = upload_video_package(folder, privacy_status="private")
    if video_id:
        print(f"✓ Uploaded: {video_id}")
    else:
        print(f"✗ Failed: {folder}")
```

## Security Best Practices

1. **Never commit credentials:**
   - `client_secrets.json` - Your OAuth credentials
   - `youtube_token.json` - Generated auth token
   - The `.gitignore` file prevents this

2. **Keep credentials secure:**
   - Don't share your `client_secrets.json` file
   - Don't expose tokens in logs or screenshots

3. **Use separate projects:**
   - Create separate Google Cloud projects for testing vs. production
   - This isolates quota and permissions

4. **Revoke access when needed:**
   - Go to [https://myaccount.google.com/permissions](https://myaccount.google.com/permissions)
   - Remove apps you no longer use

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [YouTube Data API documentation](https://developers.google.com/youtube/v3/docs)
3. Open an issue on GitHub with:
   - Error message (remove any sensitive info)
   - Steps to reproduce
   - Your Python version and OS

## Acknowledgments

- Built using [YouTube Data API v3](https://developers.google.com/youtube/v3/docs)
- Authentication via [Google Auth Library](https://github.com/googleapis/google-auth-library-python)
- Inspired by [YouTube API samples](https://github.com/youtube/api-samples)

## Disclaimer

This script is for educational and personal use. Please ensure your content complies with:
- [YouTube Terms of Service](https://www.youtube.com/t/terms)
- [YouTube Community Guidelines](https://www.youtube.com/howyoutubeworks/policies/community-guidelines/)
- Copyright laws and regulations

The authors are not responsible for any misuse of this tool.

---

**Made with ❤️ for content creators who want to automate their workflow!**
