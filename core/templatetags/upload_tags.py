from django import template
from django.urls import reverse

register = template.Library()

"""
Fonction: Convertit FileField/ImageField en URLs sécurisées via serve_upload()
Protection: Protège contre path traversal (../../.env est bloqué)

python
# Sans upload_tags:
<a href="/media/documents/conseil.pdf">  ← Accès direct, pas de contrôle

# Avec upload_tags (upload_url filter):
<a href="/fichiers/documents/conseil.pdf">  ← URL via Django, sécurisée
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
    return reverse('serve_upload', kwargs={'relative_path': name})
