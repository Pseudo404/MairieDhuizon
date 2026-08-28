from urllib.parse import quote
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class VPSMediaStorage(FileSystemStorage):
    """
    Stockage local (VPS) : en production, les URLs pointent vers /fichiers/
    servi par serve_upload(), car /media/ n'est pas exposé publiquement.
    """

    def url(self, name):
        if settings.DEBUG:
            return super().url(name)
        # Encode les caractères spéciaux (accents, espaces) dans l'URL
        encoded_name = quote(name, safe='/')
        return reverse("serve_upload", kwargs={"relative_path": encoded_name})