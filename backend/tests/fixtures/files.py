import pytest
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from pypdf import PdfWriter

@pytest.fixture
def valid_pdf():
    """Genera un PDF estructuralmente válido con pypdf."""
    buffer = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    writer.write(buffer)
    buffer.seek(0)
    return SimpleUploadedFile(
        "resume.pdf", 
        buffer.read(),
        content_type="application/pdf"
    )

@pytest.fixture
def oversized_pdf():
    """Archivo que supera los 5MB (Simulado con bytes nulos por eficiencia)."""
    size = 6 * 1024 * 1024  # 6MB
    content = b"0" * size
    return SimpleUploadedFile(
        "large.pdf", 
        content, 
        content_type="application/pdf"
    )

@pytest.fixture
def invalid_extension_file():
    """Archivo con extensión no permitida."""
    return SimpleUploadedFile(
        "virus.exe", 
        b"dummy content", 
        content_type="application/x-msdownload"
    )

@pytest.fixture
def fake_mime_pdf():
    """Archivo que dice ser PDF (.pdf) pero su contenido es texto plano."""
    return SimpleUploadedFile(
        "fake.pdf", 
        b"This is just a text file but renamed", 
        content_type="text/plain"
    )

@pytest.fixture
def invalid_signature_pdf():
    """
    Archivo que empieza con bytes aleatorios en lugar de %PDF-
    (Falla validate_pdf_signature).
    """
    content = b"\x00\x01\x02\x03" + b"Rest of content"
    return SimpleUploadedFile(
        "bad_signature.pdf", 
        content, 
        content_type="application/pdf"
    )

@pytest.fixture
def corrupted_integrity_pdf():
    """
    Archivo que tiene la firma %PDF- pero el resto es basura.
    (Falla validate_pdf_integrity porque pypdf no podrá leer páginas).
    """
    content = b"%PDF-1.4\n" + b"Not a real pdf structure"
    return SimpleUploadedFile(
        "corrupted.pdf", 
        content, 
        content_type="application/pdf"
    )