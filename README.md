# PDF Redactor - A PDF Data Masking Application

## Overview
PDF Redactor is a Flask-based web application that allows users to securely redact sensitive information from PDF files. The application automatically detects and masks names, phone numbers, email addresses, clinic names, and text in Chinese, Malaysian, and Korean languages.


## Features
- **Automatic Redaction**: Uses regex-based pattern matching to identify and mask sensitive information.
- **Language Detection**: Identifies different languages within the PDF.
- **Secure Processing**: Applies redactions directly to the PDF to ensure data privacy.
- **Simple Web Interface**: Users can upload PDFs through an intuitive Bootstrap-based UI.
- **Flask Backend**: Handles file uploads and processing efficiently

## Technologies Used
- **Frontend**:
  - HTML, CSS (Bootstrap)
  - JavaScript (for real-time clock)
- **Backend**:
  - Flask (Python)
  - PyMuPDF (Fitz) for PDF processing
  - Regex for pattern matching
  - Langid for language detection

 ## Installation and Setup
### Prerequisites
Ensure you have Python installed. You can download it from [Python.org](https://www.python.org/downloads/).

### Steps to Set Up
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/pdf-redactor.git
   cd pdf-redactor
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```sh
   pip install flask pymupdf langid
   ```

4. Run the application:
   ```sh
   python main.py
   ```

## Usage
1. Navigate to the homepage.
2. Upload a PDF file containing sensitive information.
3. The application processes the file, redacting sensitive data.
4. Download the redacted PDF.

# Contributing
Feel free to fork this repository and submit pull requests for improvements. Suggestions and feedback are welcome!

# License
This project is licensed under the MIT License.















   
