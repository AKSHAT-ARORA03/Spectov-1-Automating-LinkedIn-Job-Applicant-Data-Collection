import imaplib
import email
from email.header import decode_header
import os

EMAIL_USER = "akshatarora1299@gmail.com"
EMAIL_PASS = "waqu zmry lrpa dhev"

def connect_gmail():
    """Fetches emails labeled as 'Job Application' and saves attachments."""
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    
    # Select the "Job Application" label correctly
    status, mailbox_info = mail.select('"Job Application"', readonly=True)
    
    if status != "OK":
        print("⚠ Error: Could not access the 'Job Application' label. Check if the label exists.")
        return

    # Fetch emails under the label
    status, messages = mail.search(None, "ALL")  
    if status != "OK":
        print("⚠ Error: No emails found in 'Job Application'.")
        return

    email_ids = messages[0].split()

    processed_files = set()  # Set to track processed files

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]

                if encoding:
                    subject = subject.decode(encoding)

                print(f"📩 New Email: {subject}")

                attachments_saved = set()  # To track saved attachments

                for part in msg.walk():
                    if part.get_content_maintype() == "multipart":
                        continue
                    if part.get_content_type() == "application/pdf":  # Only PDFs
                        filename = part.get_filename()
                        if filename:
                            filename = decode_header(filename)[0][0]
                            if isinstance(filename, bytes):
                                filename = filename.decode()

                            # Check if file has been processed before
                            if filename not in processed_files:
                                processed_files.add(filename)
                                os.makedirs("resumes", exist_ok=True)  # Ensure directory exists
                                filepath = os.path.join("resumes", filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"📁 Saved Attachment: {filename}")
                            else:
                                print(f"⚠ Skipping duplicate: {filename}")

    mail.logout()
