import os
from pdfminer.high_level import extract_text as pdf_extract_text
from pdf2image import convert_from_path
import pytesseract
from docx import Document

def extract_text_from_pdf(file_path):
    try:
        text = pdf_extract_text(file_path)
        if text.strip():
            return text
    except Exception:
        pass
    # Fallback to OCR if no text extracted
    images = convert_from_path(file_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_content(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format.")
