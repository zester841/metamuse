import io
import pytesseract
import pdfplumber
import docx
import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
from PIL import Image

def extract_pdf_text(file):
    """Extract text from PDF with layout analysis and OCR fallback"""
    content = file.read()
    
    # Try text extraction first
    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
            if text.strip(): return text
    except:
        pass
    
    # OCR fallback
    images = convert_from_bytes(content)
    return "\n".join(pytesseract.image_to_string(img) for img in images)

def extract_docx_text(file):
    """Extract text from DOCX files"""
    doc = docx.Document(io.BytesIO(file.read()))
    return "\n".join(para.text for para in doc.paragraphs)

def extract_content(file):
    """Main extraction function"""
    filename = file.name.lower()
    
    if filename.endswith('.pdf'):
        return extract_pdf_text(file)
    elif filename.endswith('.docx'):
        return extract_docx_text(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise ValueError("Unsupported file format")
