# MetaMind - Automated Metadata Generator

## Features
- Extracts text from PDF, DOCX, and TXT documents
- Uses OCR for image-based PDFs
- Generates semantic metadata including:
  - Keyphrases
  - Named entities
  - Document summary
  - Readability metrics
- Web interface for document upload
- JSON metadata export

## Installation
```
git clone https://github.com/yourusername/metamind.git
cd metamind
pip install -r requirements.txt
```

## Running the App
```
streamlit run app.py
```

## Docker Deployment
```
docker build -t metamind .
docker run -p 8501:8501 metamind
```

## Usage
1. Access the web interface at `http://localhost:8501`
2. Upload a document (PDF, DOCX, or TXT)
3. View and download generated metadata
