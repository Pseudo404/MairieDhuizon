from django import template
from django.urls import reverse

register = template.Library()

"""
Convertit FileField/ImageField en URL accessible en production.

- Stockage local (VPS) : /fichiers/... via serve_upload() (sécurisé, /media/ non servi en prod)
- Cloudinary (CDN)     : URL absolue https://res.cloudinary.com/...
"""

@register.filter
def upload_url(file_field):
    if not file_field:
        return ''
    try:
        name = file_field.name
    except (AttributeError, ValueError):
        return ''
    if not name:
        return ''
    try:
        url = file_field.url
        if url.startswith(('http://', 'https://')):
            return url
    except (ValueError, AttributeError):
        pass
    return reverse('serve_upload', kwargs={'relative_path': name})
