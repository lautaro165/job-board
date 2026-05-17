import magic

from django.core.exceptions import ValidationError

MAX_RESUME_SIZE = 5 * 1024 * 1024  # 5 MB

ALLOWED_MIME_TYPES = {
    "application/pdf"
}

PDF_SIGNATURE = b"%PDF"


def validate_resume_file(file):
    RESUME_VALIDATORS = [
        validate_file_size,
        validate_pdf_extension,
        validate_pdf_mime,
        validate_pdf_signature
    ]
    
    for validator in RESUME_VALIDATORS:
        validator(file)

def validate_file_size(file):
    if file.size > MAX_RESUME_SIZE:
        raise ValidationError(
            "Resume file cannot exceed 5 MB."
        )


def validate_pdf_extension(file):
    if not file.name.lower().endswith(".pdf"):
        raise ValidationError(
            "Resume must be a PDF file."
        )


def validate_pdf_mime(file):
    mime = magic.from_buffer(
        file.read(2048),
        mime=True
    )

    file.seek(0)

    if mime not in ALLOWED_MIME_TYPES:
        raise ValidationError(
            "Invalid file type."
        )


def validate_pdf_signature(file):
    signature = file.read(4)

    file.seek(0)

    if signature != PDF_SIGNATURE:
        raise ValidationError(
            "Corrupted or invalid PDF file."
        )