# MetaMuse: Automated Metadata Generation System

![Metadata Extraction Demo](https://via.placeholder.com/800x400?text=Demo+GIF+or+Screenshot)

MetaMuse is an AI-powered document processing system that automatically extracts rich semantic metadata from documents. It transforms unstructured content into structured insights with advanced NLP and OCR capabilities.

## ✨ Key Features

- **Multi-format Support**  
  Process PDF (including scanned), DOCX, and TXT files
- **Semantic Metadata Extraction**:
  - Keyphrase identification
  - Named entity recognition
  - Abstractive summarization
  - Sentiment analysis
  - Readability classification
- **Smart Document Insights**:
  - Word/sentence statistics
  - Content categorization
  - Author/title detection
- **User-Friendly Interface**:
  - Modern web-based UI (Streamlit)
  - Real-time processing indicators
  - JSON metadata export

## Installation

### Prerequisites
- Python 3.9+
- Tesseract OCR (`sudo apt install tesseract-ocr poppler-utils` on Ubuntu)
- [Download spaCy model](https://spacy.io/models/en#en_core_web_md):  
  `python -m spacy download en_core_web_md`

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
python -m nltk.downloader stopwords
```

#### (Optional) generate your own pdf using this command. It will be generated in the output folder
```
python pdf.py
```

### 4. Run the app
```
streamlit run app.py
```

## Usage
1. Open your browser at [http://localhost:8501](http://localhost:8501)
2. Upload your document or upload from the "sample documents" directory and view/download the generated metadata.
3. you can also generate and upload your own pdf by running "python pdf.py"

## Docker (optional)
docker build -t metamind .
docker run -p 8501:8501 metamind
