import pytesseract
from pdfminer.high_level import extract_text
from pdf2image import convert_from_bytes
from docx import Document
import io

def extract_content(file_path):
    # Determine file type
    if file_path.endswith('.pdf'):
        try:
            # First try standard text extraction
            return extract_text(file_path)
        except:
            # Fallback to OCR for image-based PDFs
            with open(file_path, 'rb') as f:
                images = convert_from_bytes(f.read())
            full_text = ""
            for image in images:
                text = pytesseract.image_to_string(image)
                full_text += text + "\n"
            return full_text
    
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    else:
        raise ValueError("Unsupported file format")
