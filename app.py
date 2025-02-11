from flask import Flask, jsonify
import schedule
import threading
import time
import os

from scripts.google_sheets import process_resumes
from scripts.gmail_fetch import connect_gmail

app = Flask(__name__)

# Function to fetch emails and process resumes at startup
def fetch_and_process():
    """
    Fetch emails, process resumes, upload them to Google Drive & Sheets.
    """
    try:
        print("📩 Fetching emails...")
        connect_gmail()  # Fetch new emails and save resumes

        print("📄 Processing resumes...")
        process_resumes()  # Extract data, upload to Drive & Sheets

        print("✅ All emails processed successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

# Function to continuously run the scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(10)  # Check every second for pending tasks

# Schedule tasks (Updated to 5 minutes)
schedule.every(5).minutes.do(connect_gmail)  # Fetch emails every 5 minutes
schedule.every(5).minutes.do(process_resumes)  # Process resumes every 5 minutes

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 LinkedIn Job Automation API is running!"})

@app.route("/process_resumes", methods=["POST"])
def process_now():
    process_resumes()
    return jsonify({"message": "Resumes processed successfully!"})

@app.route("/fetch_gmail", methods=["POST"])
def fetch_gmail_now():
    connect_gmail()
    return jsonify({"message": "Emails fetched successfully!"})

if __name__ == "__main__":
    # Run fetch & process when app starts
    threading.Thread(target=fetch_and_process, daemon=True).start()

    # Start Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)