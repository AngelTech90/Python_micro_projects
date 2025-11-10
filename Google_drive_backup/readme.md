# Google Drive Auto-Backup Script

A simple and reliable Python script to automatically backup your local files to Google Drive using the Google Drive API.

## Features

- 🔐 Secure OAuth 2.0 authentication
- 📁 Automatic folder creation in Google Drive
- 🔄 Smart file updates (avoids duplicates)
- 📂 Recursive directory backup
- 💾 Token caching for seamless re-authentication
- ⚠️ Comprehensive error handling
- 📝 Well-documented code

## Prerequisites

- Python 3.7 or higher
- A Google account
- Google Cloud project with Drive API enabled

## Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/gdrive-backup.git
   cd gdrive-backup
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## Google Cloud Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on "Select a project" → "New Project"
3. Enter a project name and click "Create"

### Step 2: Enable Google Drive API

1. In the Google Cloud Console, navigate to "APIs & Services" → "Library"
2. Search for "Google Drive API"
3. Click on it and press "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, user support email)
   - Add your email to test users
   - Click "Save and Continue"
4. Select "Desktop app" as application type
5. Give it a name (e.g., "Drive Backup Desktop")
6. Click "Create"
7. Download the JSON file
8. Rename it to `credentials.json` and place it in the script directory

## Configuration

Edit the `main()` function in `backup_to_drive.py` to configure your backup:

```python
# Specify the directory you want to backup
LOCAL_DIRECTORY = "./files_to_backup"

# Specify the folder name in Google Drive
DRIVE_FOLDER_NAME = "MyBackup"
```

## Usage

### First Run

On the first run, the script will:
1. Open your default web browser
2. Ask you to sign in to your Google account
3. Request permission to access Google Drive
4. Save authentication tokens locally

```bash
python backup_to_drive.py
```

### Subsequent Runs

The script will use the saved token and run without browser interaction:

```bash
python backup_to_drive.py
```

## How It Works

1. **Authentication**: Uses OAuth 2.0 to securely authenticate with Google Drive
2. **Token Storage**: Saves authentication tokens in `token.json` for future use
3. **Folder Management**: Creates or locates the backup folder in Google Drive
4. **File Upload**: Uploads files from your local directory
5. **Smart Updates**: If a file already exists, it updates it instead of creating duplicates

## File Structure

```
gdrive-backup/
├── backup_to_drive.py      # Main script
├── credentials.json         # Your OAuth credentials (DO NOT COMMIT)
├── token.json              # Generated auth token (DO NOT COMMIT)
├── requirements.txt        # Python dependencies
├── .gitignore             # Prevents sensitive files from being committed
└── README.md              # This file
```

## Security Notes

⚠️ **IMPORTANT**: Never commit `credentials.json` or `token.json` to version control!

The `.gitignore` file is configured to prevent these files from being accidentally committed:

```gitignore
credentials.json
token.json
*.pyc
__pycache__/
```

## Troubleshooting

### "credentials.json not found" error
- Make sure you've downloaded the OAuth credentials from Google Cloud Console
- Ensure the file is named exactly `credentials.json`
- Place it in the same directory as the script

### "Invalid grant" error
- Delete `token.json` and run the script again
- Re-authenticate when prompted

### "Access denied" error
- Ensure the Google Drive API is enabled in your project
- Check that you've added your email as a test user in the OAuth consent screen

### Files not uploading
- Check that the local directory path is correct
- Verify you have read permissions for the files
- Ensure you have enough Google Drive storage space

## Customization

### Backup Specific File Types

Modify the `backup_directory()` function to filter files:

```python
for file_path in local_path.rglob('*.pdf'):  # Only backup PDFs
    if file_path.is_file():
        upload_file(service, str(file_path), folder_id)
```

### Schedule Automatic Backups

**Linux/Mac (using cron):**
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/backup_to_drive.py
```

**Windows (using Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly, etc.)
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: full path to `backup_to_drive.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- Built using [Google Drive API v3](https://developers.google.com/drive/api/v3/about-sdk)
- Authentication via [Google Auth Library](https://github.com/googleapis/google-auth-library-python)

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the [Google Drive API documentation](https://developers.google.com/drive/api/v3/reference)

---

**Note**: This script requires internet connection to communicate with Google Drive API.