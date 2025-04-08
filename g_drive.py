# pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io

# Path to your service account key file
SERVICE_ACCOUNT_FILE = r'credentials file path'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate with the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

# Folder ID from the shared link
FOLDER_ID = 'folder id'

def list_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def download_file(file_id, file_name):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {file_name}: {int(status.progress() * 100)}%")

def main():
    files = list_files_in_folder(FOLDER_ID)
    print("Files in folder:")
    for file in files:
        print(f"Name: {file['name']}, ID: {file['id']}")
        # Example: Download each file
        download_file(file['id'], file['name'])

if __name__ == '__main__':
    main()
