from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

# Google Drive API Setup
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = "credentials/service_account.json"  # Ensure this file exists

# 🔹 Replace this with your Google Drive "Resume" folder ID
RESUME_FOLDER_ID = "1kIMiEZyGFbJ0B9hXAl7rTRQoshxliD08"  # 🔴 CHANGE THIS TO YOUR FOLDER ID

def authenticate_drive():
    """Authenticate with Google Drive using a service account."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("drive", "v3", credentials=credentials)
        return service
    except Exception as e:
        print(f"❌ Error authenticating with Google Drive: {e}")
        return None

def upload_file(file_path, folder_id=RESUME_FOLDER_ID):
    """
    Uploads a file to Google Drive inside the specified folder.
    
    :param file_path: Path of the file to be uploaded
    :param folder_id: Google Drive folder ID (default: Resume folder)
    :return: Shareable link of the uploaded file
    """
    service = authenticate_drive()
    if not service:
        return None

    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        file_id = file.get("id")

        # Make the file publicly accessible
        service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"},
        ).execute()

        shareable_link = f"https://drive.google.com/file/d/{file_id}/view"
        print(f"✅ Uploaded '{file_path}' successfully. Shareable Link: {shareable_link}")
        return shareable_link
    except Exception as e:
        print(f"❌ Failed to upload file: {e}")
        return None

def list_drive_files():
    """Lists files in Google Drive inside the 'Resume' folder."""
    service = authenticate_drive()
    if not service:
        return []

    try:
        query = f"'{RESUME_FOLDER_ID}' in parents"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])

        if not files:
            print("📂 No files found in the 'Resume' folder.")
        else:
            print("📂 Files in Drive (Resume folder):")
            for file in files:
                print(f"📄 {file['name']} (ID: {file['id']})")

        return files
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []

if __name__ == "__main__":
    list_drive_files()  # List all files in Resume folder

    # Example: Upload a sample resume to the Resume folder
    sample_pdf_path = "resumes/sample_resume.pdf"  # Replace with your actual resume file path
    if os.path.exists(sample_pdf_path):
        upload_file(sample_pdf_path)
    else:
        print(f"⚠️ File '{sample_pdf_path}' not found. Please add a resume in the 'resumes' folder.")
