from django import template

register = template.Library()

"""
Convertit FileField/ImageField en URL accessible en production.

- Stockage local (VPS) : /fichiers/... via VPSMediaStorage + serve_upload()
- Cloudinary (CDN)     : URL absolue https://res.cloudinary.com/...
"""

@register.filter
def upload_url(file_field):
    if not file_field:
        return ''
    try:
        return file_field.url
    except (AttributeError, ValueError):
        return ''
