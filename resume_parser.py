"""
resume_parser.py
Extracts plain text from uploaded PDF or TXT resume files.
"""

import PyPDF2
import io


def extract_text_from_pdf(pdf_file) -> str:
    """
    Accepts a file-like object (from st.file_uploader) and returns
    all text extracted from the PDF pages as a single string.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())
        return "\n".join(pages_text)
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")


def extract_text_from_txt(txt_file) -> str:
    """
    Accepts a file-like object (from st.file_uploader) and returns
    the decoded text content.
    """
    try:
        return txt_file.read().decode("utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read TXT file: {e}")


def parse_resume(uploaded_file) -> str:
    """
    Auto-detects file type and routes to the correct extractor.
    Returns the resume as a plain string.
    """
    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")
