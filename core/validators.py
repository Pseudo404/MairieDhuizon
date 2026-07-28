import re
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp', 'gif']
ALLOWED_PDF_EXTENSIONS = ['pdf']
ALLOWED_DOCUMENT_EXTENSIONS = ['pdf', 'jpg', 'jpeg', 'png', 'webp', 'gif']

validate_image_upload = FileExtensionValidator(
    allowed_extensions=ALLOWED_IMAGE_EXTENSIONS,
    message='Format image non autorisé. Utilisez : JPG, PNG, WEBP ou GIF.',
)
validate_pdf_upload = FileExtensionValidator(
    allowed_extensions=ALLOWED_PDF_EXTENSIONS,
    message='Seuls les fichiers PDF sont autorisés.',
)
validate_document_upload = FileExtensionValidator(
    allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS,
    message='Format non autorisé. Utilisez : PDF, JPG, PNG ou WEBP.',
)

_UNSAFE_URL_SCHEMES = re.compile(r'^(javascript|data|vbscript):', re.I) # interdi d'avoir dans le lien "javascript:", "data:" ou "vbscript:", XSS

def validate_safe_link_url(value):
    if not value or not str(value).strip():
        return
    url = str(value).strip()
    if _UNSAFE_URL_SCHEMES.match(url):
        raise ValidationError("Ce type de lien n'est pas autorisé.")
    if url.startswith('/') or url.startswith('#'):
        return
    if url.startswith('http://') or url.startswith('https://'):
        return
    raise ValidationError('Le lien doit commencer par /, http:// ou https://.')

def sanitize_email_header(value, max_length=200):
    """Email Header Injection"""
    if not value:
        return ''
    cleaned = str(value).replace('\r', '').replace('\n', '').strip()
    return cleaned[:max_length]
