# utils.py - helper functions for parsing and exports
import re, io, json
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    pages = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(pages)

def extract_text_from_docx(file_stream):
    doc = Document(file_stream)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def normalize_text(text):
    return re.sub(r"\s+", " ", text).strip()

def export_session_json(session):
    # session is dict; return BytesIO
    b = io.BytesIO()
    b.write(json.dumps(session, indent=2).encode('utf-8'))
    b.seek(0)
    return b
