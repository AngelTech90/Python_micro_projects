"""
YouTube Video Auto-Upload Script
==================================
This script automatically uploads videos to YouTube with custom metadata (title, description, 
thumbnail, tags) using the YouTube Data API v3.

Prerequisites:
1. Install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
2. Enable YouTube Data API v3 in Google Cloud Console
3. Create OAuth 2.0 credentials and download client_secrets.json
4. Place client_secrets.json in the same directory as this script
5. Your YouTube channel must be verified to upload custom thumbnails

Important Notes:
- If your app is in "Testing" mode (not published), uploaded videos will be locked as "Private"
- To upload public videos, you must publish your OAuth app in Google Cloud Console
- For personal use in testing mode, you can manually change video privacy in YouTube Studio after upload
- Default quota allows approximately 6 video uploads per day (1600 units per upload)

Author: Your Name
Repository: https://github.com/yourusername/youtube-auto-uploader
"""

import os
import json
import time
import random
import http.client
import httplib2
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# YouTube API Configuration
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# File paths for OAuth credentials and tokens
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_FILE = "youtube_token.json"

# Retry configuration for handling network issues during upload
RETRIABLE_EXCEPTIONS = (
    httplib2.HttpLib2Error,
    IOError,
    http.client.NotConnected,
    http.client.IncompleteRead,
    http.client.ImproperConnectionState,
    http.client.CannotSendRequest,
    http.client.CannotSendHeader,
    http.client.ResponseNotReady,
    http.client.BadStatusLine,
)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
MAX_RETRIES = 10


def authenticate_youtube():
    """
    Authenticate with YouTube Data API using OAuth 2.0.
    
    Returns:
        youtube: Authorized YouTube API service instance
    """
    creds = None
    
    # Check if token file exists (stores user's access and refresh tokens)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, [YOUTUBE_UPLOAD_SCOPE])
    
    # If credentials don't exist or are invalid, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Run OAuth flow for new credentials
            if not os.path.exists(CLIENT_SECRETS_FILE):
                raise FileNotFoundError(
                    f"{CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, [YOUTUBE_UPLOAD_SCOPE]
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Build and return the YouTube service
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds)
    return youtube


def read_text_file(file_path):
    """
    Read and return the contents of a text file.
    
    Args:
        file_path: Path to the text file
    
    Returns:
        content: File content as string, or None if file doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def parse_tags(tags_text):
    """
    Parse tags from text. Accepts comma-separated or space-separated tags.
    
    Args:
        tags_text: String containing tags
    
    Returns:
        list: List of tag strings
    """
    if not tags_text:
        return []
    
    # Try comma-separated first
    if ',' in tags_text:
        tags = [tag.strip() for tag in tags_text.split(',')]
    else:
        # Fall back to space-separated
        tags = [tag.strip() for tag in tags_text.split()]
    
    # Filter out empty tags and ensure they start with # for hashtags
    cleaned_tags = []
    for tag in tags:
        tag = tag.strip()
        if tag:
            # Remove # if present (YouTube API doesn't need it in tags array)
            if tag.startswith('#'):
                tag = tag[1:]
            if tag:  # Check again after removing #
                cleaned_tags.append(tag)
    
    return cleaned_tags


def resumable_upload(request):
    """
    Execute video upload with exponential backoff retry strategy.
    This handles network interruptions and temporary server errors.
    
    Args:
        request: MediaFileUpload request object
    
    Returns:
        response: YouTube API response with video details
    """
    response = None
    error = None
    retry = 0
    
    while response is None:
        try:
            print("Uploading video...")
            status, response = request.next_chunk()
            
            if response is not None:
                if 'id' in response:
                    print(f"Video uploaded successfully! Video ID: {response['id']}")
                    return response
                else:
                    raise Exception(f"Unexpected response: {response}")
            
            # Show upload progress
            if status:
                progress = int(status.progress() * 100)
                print(f"Upload progress: {progress}%")
                
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"
        
        # Handle retry logic with exponential backoff
        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception("Maximum number of retries exceeded.")
            
            # Exponential backoff: wait 2^retry seconds plus random jitter
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f"Retrying in {sleep_seconds:.2f} seconds...")
            time.sleep(sleep_seconds)


def upload_video(youtube, video_path, title, description, tags, category_id="22", privacy_status="private"):
    """
    Upload a video to YouTube with specified metadata.
    
    Args:
        youtube: Authorized YouTube API service instance
        video_path: Path to the video file (.mp4, .mov, .avi, etc.)
        title: Video title (max 100 characters)
        description: Video description (max 5000 characters)
        tags: List of tags (max 500 characters total)
        category_id: YouTube category ID (default "22" = People & Blogs)
        privacy_status: "public", "private", or "unlisted"
    
    Returns:
        video_id: ID of the uploaded video, or None if failed
    
    Category IDs reference:
        1=Film & Animation, 2=Autos & Vehicles, 10=Music, 15=Pets & Animals,
        17=Sports, 19=Travel & Events, 20=Gaming, 22=People & Blogs,
        23=Comedy, 24=Entertainment, 25=News & Politics, 26=Howto & Style,
        27=Education, 28=Science & Technology
    """
    try:
        # Validate video file exists
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title[:100],  # YouTube limit: 100 characters
                'description': description[:5000],  # YouTube limit: 5000 characters
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False  # Set to True if content is for kids
            }
        }
        
        # Create media upload object with resumable upload enabled
        media = MediaFileUpload(
            video_path,
            chunksize=-1,  # -1 means upload in a single request (faster for small files)
            resumable=True,
            mimetype='video/*'
        )
        
        # Execute the upload request
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media_body=media
        )
        
        # Upload with retry logic
        response = resumable_upload(request)
        
        if response and 'id' in response:
            return response['id']
        return None
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e.resp.status}\n{e.content}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def upload_thumbnail(youtube, video_id, thumbnail_path):
    """
    Upload and set a custom thumbnail for a YouTube video.
    
    Note: Your YouTube channel must be verified to use custom thumbnails.
    Verify at: https://www.youtube.com/verify
    
    Args:
        youtube: Authorized YouTube API service instance
        video_id: ID of the video to set thumbnail for
        thumbnail_path: Path to thumbnail image (.png, .jpg - max 2MB)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(thumbnail_path):
            print(f"Thumbnail file not found: {thumbnail_path}")
            return False
        
        # Check file size (YouTube limit: 2MB)
        file_size = os.path.getsize(thumbnail_path)
        if file_size > 2 * 1024 * 1024:  # 2MB in bytes
            print(f"Thumbnail file too large ({file_size / 1024 / 1024:.2f}MB). Maximum is 2MB.")
            return False
        
        print(f"Uploading thumbnail for video ID: {video_id}...")
        
        # Create media upload for thumbnail
        media = MediaFileUpload(thumbnail_path, mimetype='image/png', resumable=True)
        
        # Execute thumbnail upload
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=media
        )
        
        response = request.execute()
        print("Thumbnail uploaded successfully!")
        return True
        
    except HttpError as e:
        # Common error: Channel not verified for custom thumbnails
        if e.resp.status == 403:
            print("\nError 403: Unable to upload thumbnail.")
            print("Your YouTube channel must be verified to upload custom thumbnails.")
            print("Verify your channel at: https://www.youtube.com/verify")
        else:
            print(f"An HTTP error occurred: {e.resp.status}\n{e.content}")
        return False
    except Exception as e:
        print(f"An error occurred uploading thumbnail: {e}")
        return False


def upload_video_package(video_folder, privacy_status="private", category_id="22"):
    """
    Upload a complete video package (video + metadata + thumbnail).
    
    Expected folder structure:
        video_folder/
            ├── video.mp4        (or .mov, .avi, etc.)
            ├── title.txt        (video title)
            ├── description.txt  (video description)
            ├── tags.txt         (comma or space-separated tags/hashtags)
            └── thumbnail.png    (or .jpg)
    
    Args:
        video_folder: Path to folder containing all video assets
        privacy_status: "public", "private", or "unlisted"
        category_id: YouTube category ID (see upload_video() for reference)
    
    Returns:
        video_id: ID of uploaded video, or None if failed
    """
    folder_path = Path(video_folder)
    
    if not folder_path.exists():
        print(f"Error: Folder not found: {video_folder}")
        return None
    
    print(f"\n{'='*60}")
    print(f"Processing video package: {folder_path.name}")
    print(f"{'='*60}\n")
    
    # Find video file (supports multiple formats)
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv']
    video_file = None
    for ext in video_extensions:
        candidates = list(folder_path.glob(f'*{ext}'))
        if candidates:
            video_file = candidates[0]
            break
    
    if not video_file:
        print(f"Error: No video file found in {video_folder}")
        print(f"Supported formats: {', '.join(video_extensions)}")
        return None
    
    print(f"✓ Found video: {video_file.name}")
    
    # Read metadata files
    title = read_text_file(folder_path / "title.txt")
    description = read_text_file(folder_path / "description.txt")
    tags_text = read_text_file(folder_path / "tags.txt")
    
    # Use filename as fallback for title
    if not title:
        title = video_file.stem
        print(f"⚠ No title.txt found, using filename: {title}")
    else:
        print(f"✓ Title: {title}")
    
    # Use empty description if not provided
    if not description:
        description = ""
        print("⚠ No description.txt found, using empty description")
    else:
        print(f"✓ Description loaded ({len(description)} characters)")
    
    # Parse tags
    tags = parse_tags(tags_text)
    if tags:
        print(f"✓ Tags: {', '.join(tags)}")
    else:
        print("⚠ No tags.txt found or no valid tags")
    
    # Find thumbnail file
    thumbnail_extensions = ['.png', '.jpg', '.jpeg']
    thumbnail_file = None
    for ext in thumbnail_extensions:
        candidates = list(folder_path.glob(f'*{ext}'))
        if candidates:
            thumbnail_file = candidates[0]
            break
    
    if thumbnail_file:
        print(f"✓ Found thumbnail: {thumbnail_file.name}")
    else:
        print("⚠ No thumbnail found (optional)")
    
    # Authenticate with YouTube
    print("\nAuthenticating with YouTube...")
    youtube = authenticate_youtube()
    print("✓ Authentication successful!")
    
    # Upload video
    print(f"\nUploading video (privacy: {privacy_status})...")
    video_id = upload_video(
        youtube,
        str(video_file),
        title,
        description,
        tags,
        category_id,
        privacy_status
    )
    
    if not video_id:
        print("❌ Video upload failed!")
        return None
    
    print(f"✓ Video uploaded! ID: {video_id}")
    print(f"   Watch at: https://www.youtube.com/watch?v={video_id}")
    
    # Upload thumbnail if available
    if thumbnail_file:
        print("\nUploading thumbnail...")
        success = upload_thumbnail(youtube, video_id, str(thumbnail_file))
        if success:
            print("✓ Thumbnail uploaded!")
        else:
            print("⚠ Thumbnail upload failed (video still uploaded successfully)")
    
    print(f"\n{'='*60}")
    print("Upload complete!")
    print(f"{'='*60}\n")
    
    return video_id


def main():
    """
    Main function - Configure your upload here.
    """
    print("YouTube Video Auto-Upload Script")
    print("=" * 60)
    
    # CONFIGURATION - Modify these values for your use case
    # =========================================================
    
    # Path to folder containing your video package
    VIDEO_FOLDER = "./video_package"
    
    # Privacy status: "public", "private", or "unlisted"
    # NOTE: If app is in Testing mode, videos will be locked as Private
    PRIVACY_STATUS = "private"
    
    # Category ID (see upload_video() docstring for full list)
    CATEGORY_ID = "22"  # People & Blogs
    
    # =========================================================
    
    # Execute upload
    video_id = upload_video_package(
        VIDEO_FOLDER,
        privacy_status=PRIVACY_STATUS,
        category_id=CATEGORY_ID
    )
    
    if video_id:
        print("\n✅ SUCCESS! Your video has been uploaded.")
        print(f"Video ID: {video_id}")
        print(f"URL: https://www.youtube.com/watch?v={video_id}")
        
        if PRIVACY_STATUS == "private":
            print("\n💡 TIP: If you want to make this video public, you can:")
            print("   1. Publish your OAuth app in Google Cloud Console, OR")
            print("   2. Manually change the privacy setting in YouTube Studio")
    else:
        print("\n❌ Upload failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
