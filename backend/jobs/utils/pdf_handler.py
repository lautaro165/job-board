import pypdf
from io import BytesIO

def extract_text_from_pdf(pdf_file):
    try:
        current_cursor = pdf_file.tell()
        
        pdf_file.seek(0)
        reader = pypdf.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        pdf_file.seek(current_cursor)
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"