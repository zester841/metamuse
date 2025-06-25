# MetaMuse: Automated Metadata Generation System

## Features
- Extracts text from PDF, DOCX, and TXT (with OCR fallback for PDFs)
- Generates semantic metadata:
  - Keyphrases
  - Named entities
  - Abstractive summary
  - Sentiment & readability analysis
  - Document statistics
- Clean, modern Streamlit web interface
- Downloadable JSON metadata

## Installation
### 1. Clone the repository

```
git clone https://github.com/yourusername/metamind.git
cd metamind
```

### 2. Set up a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
```


### 3. Install dependencies
```
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

**Install system dependencies:**
- Ubuntu: `sudo apt-get install tesseract-ocr poppler-utils`
- Windows: Download [Tesseract](https://github.com/tesseract-ocr/tesseract) and [Poppler](http://blog.alivate.com.au/poppler-windows/) binaries and add to PATH.

### 4. Run the app
```
streamlit run app.py
```

## Usage
1. Open your browser at [http://localhost:8501](http://localhost:8501)
2. Upload your document and view/download the generated metadata.

## Docker (optional)
docker build -t metamind .
docker run -p 8501:8501 metamind
