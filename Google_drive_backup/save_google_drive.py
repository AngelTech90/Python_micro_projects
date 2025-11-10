# in this script we'll automate upload of our backups to google drive:
"""
Google Drive Auto-Backup Script
================================
This script automatically backs up local files to Google Drive using the Google Drive API.

Prerequisites:
1. Install required packages: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
2. Enable Google Drive API in Google Cloud Console
3. Create OAuth 2.0 credentials and download credentials.json
4. Place credentials.json in the same directory as this script

Author: Your Name
License: MIT
"""

import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Define the scope for Google Drive access
# If modifying these scopes, delete the token.json file
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Configuration file path (you can modify this)
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'


def authenticate_google_drive():
    """
    Authenticate with Google Drive API using OAuth 2.0.
    
    Returns:
        service: Authorized Google Drive API service instance
    """
    creds = None
    
    # Check if token.json exists (stores user's access and refresh tokens)
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If credentials don't exist or are invalid, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            creds.refresh(Request())
        else:
            # Run OAuth flow for new credentials
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"{CREDENTIALS_FILE} not found. Please download it from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Build and return the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    return service


def get_or_create_folder(service, folder_name, parent_id=None):
    """
    Get existing folder ID or create a new folder in Google Drive.
    
    Args:
        service: Authorized Google Drive API service instance
        folder_name: Name of the folder to create/find
        parent_id: Parent folder ID (None for root)
    
    Returns:
        folder_id: ID of the folder
    """
    try:
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        if folders:
            # Folder exists, return its ID
            print(f"Folder '{folder_name}' already exists.")
            return folders[0]['id']
        
        # Create new folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Created folder '{folder_name}'.")
        return folder.get('id')
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def upload_file(service, file_path, folder_id=None):
    """
    Upload a file to Google Drive.
    
    Args:
        service: Authorized Google Drive API service instance
        file_path: Path to the local file to upload
        folder_id: ID of the Google Drive folder (None for root)
    
    Returns:
        file_id: ID of the uploaded file, or None if failed
    """
    try:
        file_name = os.path.basename(file_path)
        
        # Prepare file metadata
        file_metadata = {'name': file_name}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Create media upload object
        media = MediaFileUpload(file_path, resumable=True)
        
        # Check if file already exists
        query = f"name='{file_name}' and trashed=false"
        if folder_id:
            query += f" and '{folder_id}' in parents"
        
        results = service.files().list(q=query, fields="files(id, name)").execute()
        existing_files = results.get('files', [])
        
        if existing_files:
            # Update existing file
            file_id = existing_files[0]['id']
            updated_file = service.files().update(
                fileId=file_id,
                media_body=media
            ).execute()
            print(f"Updated: {file_name}")
            return updated_file.get('id')
        else:
            # Upload new file
            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"Uploaded: {file_name}")
            return uploaded_file.get('id')
    
    except HttpError as error:
        print(f"Error uploading {file_path}: {error}")
        return None


def backup_directory(service, local_dir, drive_folder_name="Backup"):
    """
    Backup an entire directory to Google Drive.
    
    Args:
        service: Authorized Google Drive API service instance
        local_dir: Path to the local directory to backup
        drive_folder_name: Name of the folder in Google Drive
    """
    # Create or get the backup folder in Google Drive
    folder_id = get_or_create_folder(service, drive_folder_name)
    
    if not folder_id:
        print("Failed to create/access backup folder.")
        return
    
    # Get all files in the local directory
    local_path = Path(local_dir)
    if not local_path.exists():
        print(f"Directory {local_dir} does not exist.")
        return
    
    # Upload each file
    uploaded_count = 0
    for file_path in local_path.rglob('*'):
        if file_path.is_file():
            result = upload_file(service, str(file_path), folder_id)
            if result:
                uploaded_count += 1
    
    print(f"\nBackup complete! {uploaded_count} files processed.")


def main():
    """
    Main function to run the backup script.
    """
    print("Google Drive Auto-Backup Script")
    print("=" * 40)
    
    # Authenticate with Google Drive
    print("\nAuthenticating with Google Drive...")
    service = authenticate_google_drive()
    print("Authentication successful!")
    
    # Example usage: Backup a specific directory
    # Modify these variables according to your needs
    LOCAL_DIRECTORY = "./files_to_backup"  # Change this to your directory
    DRIVE_FOLDER_NAME = "MyBackup"  # Change this to your preferred folder name
    
    print(f"\nStarting backup of: {LOCAL_DIRECTORY}")
    print(f"Destination folder: {DRIVE_FOLDER_NAME}")
    
    backup_directory(service, LOCAL_DIRECTORY, DRIVE_FOLDER_NAME)


if __name__ == "__main__":
    main()