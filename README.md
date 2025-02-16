# LinkedIn Job Automation

## Overview
This project automates LinkedIn job applications using Google Sheets for managing applicant data. It fetches real-time applicant details and displays them on a dashboard.

## Project Structure
```
linkedin_job_automation/
 ┣ credentials/
 ┃ ┗ credentials.json  # Google API credentials
 ┣ resumes/           # Store resumes
 ┣ scripts/
 ┃ ┣ gmail_fetch.py   # Fetch emails from Gmail
 ┃ ┣ google_drive.py  # Upload/download files from Google Drive
 ┃ ┣ google_sheets.py # Interact with Google Sheets
 ┃ ┣ index.html       # Frontend dashboard
 ┃ ┣ script.js        # Fetch and display data
 ┃ ┣ style.css        # Styling for dashboard
 ┣ venv/              # Virtual environment
 ┣ app.py             # Backend server
 ┣ .env               # Environment variables (Google API Key)
 ┗ README.md
```

## Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Node.js & npm
- Virtual Environment (optional but recommended)

## Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/linkedin_job_automation.git
cd linkedin_job_automation
```

### 2. Set Up Virtual Environment (Python)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Set Up Google API Credentials
- Place `credentials.json` inside the `credentials/` folder.
- Set up Google Sheets, Drive, and Gmail API permissions.

### 4. Create a `.env` File
Create a `.env` file in the root folder and add:
```env
REACT_APP_API_KEY=your_google_api_key_here
```

## Running the Project
### 1. Start the Backend Server
```bash
python app.py
```
The backend serves API keys and interacts with Google services.

### 2. Start the Frontend (Dashboard)
```bash
cd scripts
python -m http.server 8000
```
Visit `http://localhost:8000` in a browser.

## Features
- **Gmail Fetching**: Retrieves job application emails.
- **Google Sheets Integration**: Stores applicant data.
- **Google Drive Uploads**: Saves resumes to Drive.
- **Real-Time Dashboard**: Displays applicant details dynamically.

## Troubleshooting
- **404 Error (File Not Found)**: Ensure the correct file paths in `script.js`.
- **403 Forbidden (Google API)**: Check API key permissions.
- **CORS Issues**: Use `cors` middleware in the backend if required.

## Future Improvements
- Add authentication for API access.
- Enhance the UI with better styling.
- Automate LinkedIn job applications further.

## License
MIT License

To know how to set up ,see this video below
https://youtu.be/LyMRDKxI-vU?si=mv0lZ1OLyBUuPmD7
