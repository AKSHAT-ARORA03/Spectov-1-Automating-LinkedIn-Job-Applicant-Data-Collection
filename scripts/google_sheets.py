import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pdfplumber
import re
import os

# Google Sheets API setup
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = r"C:\Users\aksha\Desktop\linkedin_job_automation\credentials\credentials.json"
SHEET_ID = "1OntEp66GXDfsbt2fqLWZ9qqZ6QJPzQctMkPqg-zlQTE"
FOLDER_ID = "1kIMiEZyGFbJ0B9hXAl7rTRQoshxliD08"  # Replace with your Google Drive folder ID

# Authenticate Google APIs
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1
drive_service = build("drive", "v3", credentials=creds)

def get_existing_data():
    """Fetch all existing names, emails, and resume links from Google Sheets."""
    try:
        records = sheet.get_all_values()[1:]  # Skip headers
        return {(row[0], row[1]): row[3] for row in records if len(row) >= 4}  # (name, email) -> resume_link
    except Exception as e:
        print(f"❌ Error fetching existing data from Google Sheets: {e}")
        return {}

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    except Exception as e:
        print(f"❌ Error reading PDF {pdf_path}: {e}")
        return ""

def extract_details(text):
    """Extracts Name, Email, and Phone from resume text."""
    lines = text.split("\n")
    name = lines[0] if lines else "N/A"

    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"\+?\d[\d\s-]{8,15}\d", text)

    email = email_match.group() if email_match else "N/A"
    phone = phone_match.group() if phone_match else "N/A"

    return name, email, phone

def check_duplicate_in_drive(pdf_filename):
    """Check if a resume with the same filename already exists in Google Drive."""
    try:
        query = f"'{FOLDER_ID}' in parents and name = '{pdf_filename}' and mimeType = 'application/pdf'"
        response = drive_service.files().list(q=query, fields="files(id, webViewLink)").execute()
        files = response.get("files", [])

        if files:
            print(f"⚠ Resume '{pdf_filename}' already exists in Google Drive. Skipping upload.")
            return files[0]["webViewLink"]
        return None

    except Exception as e:
        print(f"❌ Error checking duplicate in Google Drive: {e}")
        return None

def upload_to_drive(pdf_path):
    """Uploads PDF to Google Drive and returns shareable link."""
    filename = os.path.basename(pdf_path)

    # Check if file already exists in Google Drive
    existing_link = check_duplicate_in_drive(filename)
    if existing_link:
        return existing_link  # Return existing link without uploading again

    file_metadata = {
        "name": filename,
        "parents": [FOLDER_ID],
        "mimeType": "application/pdf"
    }

    try:
        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_id = file.get("id")
        if not file_id:
            print("❌ Failed to upload file to Google Drive.")
            return "N/A"

        # Make file shareable
        drive_service.permissions().create(
            fileId=file_id,
            body={"role": "reader", "type": "anyone"},
        ).execute()

        shareable_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        print(f"✅ Uploaded to Google Drive: {shareable_link}")
        return shareable_link

    except Exception as e:
        print(f"❌ Google Drive upload error: {e}")
        return "N/A"

def upload_to_sheets(name, email, phone, resume_link, existing_data):
    """Uploads extracted data to Google Sheets, avoiding duplicates."""
    if (name, email) in existing_data:
        print(f"⚠ Duplicate entry for {name} ({email}) found. Skipping Google Sheets upload.")
        return

    try:
        sheet.append_row([name, email, phone, resume_link])
        print(f"✅ Added {name} to Google Sheets.")
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")

def process_resumes():
    """Processes all PDF resumes in the folder."""
    folder_path = "resumes"

    if not os.path.exists(folder_path):
        print("❌ Resumes folder not found!")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    if not pdf_files:
        print("❌ No resumes found!")
        return

    existing_data = get_existing_data()  # Fetch existing names, emails, and resume links

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"📄 Processing: {pdf_file}")

        text = extract_text_from_pdf(pdf_path)
        if not text.strip():
            print(f"⚠ Skipping {pdf_file} due to empty text extraction.")
            continue

        name, email, phone = extract_details(text)

        # Check if resume with this name/email is already uploaded in Google Sheets
        if (name, email) in existing_data:
            print(f"⚠ Duplicate entry for {name} ({email}) found in Google Sheets. Skipping upload.")
            continue

        resume_link = upload_to_drive(pdf_path)
        upload_to_sheets(name, email, phone, resume_link, existing_data)

    print("✅ All resumes processed successfully!")
