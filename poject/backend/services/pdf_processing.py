# backend/services/pdf_processing.py
import os
import pymupdf4llm

def extract_pdf_text(file, pages_param=None):
    """Extract text from a PDF file."""
    # Save the file temporarily
    temp_folder = os.getenv("TEMP_FOLDER", "temp")
    os.makedirs(temp_folder, exist_ok=True)
    file_path = os.path.join(temp_folder, file.filename)
    file.save(file_path)

    try:
        # Parse pages parameter
        pages = None
        if pages_param:
            pages = parse_pages_param(pages_param)

        # Extract text using pymupdf4llm
        md_text = pymupdf4llm.to_markdown(file_path, pages=pages)
        return md_text
    except Exception as e:
        raise ValueError(f"Error extracting text: {e}")
    finally:
        # Clean up temporary file
        os.remove(file_path)

def parse_pages_param(pages_param):
    """Parse a pages parameter into a list of page numbers."""
    try:
        if "-" in pages_param:
            start, end = map(int, pages_param.split("-"))
            return list(range(start, end + 1))
        else:
            # Split by comma for individual pages
            return [int(p.strip()) for p in pages_param.split(",") if p.strip().isdigit()]
    except ValueError:
        raise ValueError(f"Invalid pages parameter: {pages_param}")
