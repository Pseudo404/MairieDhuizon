import mimetypes
from pathlib import Path
from urllib.parse import unquote
from django.conf import settings
from django.http import FileResponse, Http404

def _safe_media_path(relative_path: str) -> Path:
    # Décode les caractères encodés dans l'URL (%C3%A9 → é)
    relative_path = unquote(relative_path)
    
    if not relative_path or '..' in relative_path:
        raise Http404
    media_root = Path(settings.MEDIA_ROOT).resolve()
    full_path = (media_root / relative_path).resolve()
    try:
        full_path.relative_to(media_root)
    except ValueError:
        raise Http404
    if not full_path.is_file():
        raise Http404
    return full_path

def file_response_for_path(relative_path: str, download_name: str | None = None) -> FileResponse:
    full_path = _safe_media_path(relative_path)
    content_type, _ = mimetypes.guess_type(str(full_path))
    if not content_type:
        content_type = 'application/octet-stream'
    response = FileResponse(
        full_path.open('rb'),
        content_type=content_type,
        as_attachment=False,
        filename=download_name or full_path.name,
    )
    if content_type == 'application/pdf':
        response['Content-Disposition'] = f'inline; filename="{full_path.name}"'
    return response