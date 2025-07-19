# Quick Start Guide

This guide will help you get started with the Police Case Management System quickly.

## System Requirements

- Python 3.8 or higher
- SQL Server LocalDB
- 4GB RAM minimum
- 2GB free disk space

## Installation Steps

1. **Install required packages:**

```powershell
pip install -r requirements.txt
```

2. **Initialize the database:**

The application will automatically create the database and tables when you run it for the first time. Make sure SQL Server LocalDB is installed and running on your system.

3. **Start the application:**

```powershell
python run.py
```

4. **Access the application:**

Open your browser and go to: http://localhost:5000

## Initial Setup

1. **Create an account:**
   - Go to the Sign Up page
   - Use one of the authorized email addresses:
     - kuncharapuranjith@gmail.com
     - ranjith888999@gmail.com
   - Set a password (default test password is 123456)

2. **Log in:**
   - Use your email and password to log in
   - You will be redirected to the dashboard

3. **Upload documents:**
   - Click on the "Admin" link in the top navigation
   - Use the upload form to add documents
   - Specify the document type:
     - Case Section Analysis
     - Bail Analysis
     - Human Analysis

4. **Start analyzing:**
   - Return to the dashboard
   - Choose the analysis type you want to work with
   - For Case Section Analysis, enter case details and submit
   - For Bail Analysis and Human Analysis, use the chat interface to ask questions

## Troubleshooting

- **Database connection issues:**
  - Make sure SQL Server LocalDB is running
  - Check that the connection string in `app/models/database.py` is correct

- **Document upload failures:**
  - Ensure the `app/static/uploads` directory exists and is writable
  - Check that your document format is supported (PDF, DOCX, TXT, CSV, XLSX)

- **AI response issues:**
  - Verify your internet connection (required for Gemini AI)
  - Ensure the API key for Google Gemini is valid

For more detailed information, refer to the full documentation or contact support.
