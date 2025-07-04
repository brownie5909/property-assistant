from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

def upload_file_to_drive(filename):
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': filename,
        'parents': ['1tXpD4m4CZmE66tViE7ye9IGJrEvtve52']  # Google Drive folder ID
    }
    media = MediaFileUpload(filename, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    return f"https://drive.google.com/file/d/{file_id}/view"
