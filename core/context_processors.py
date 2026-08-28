"""
Context processor – logo du site

Injecte automatiquement la variable `site_logo_url` dans tous les templates.
Si un logo est uploade dans CommuneInfo, son URL est construite via la route /fichiers/
(qui fonctionne en production). Sinon None (fallback vers le statique).
"""


def site_logo(request):
    """Rend l'URL du logo de la commune disponible dans tous les templates."""
    try:
        from core.models import CommuneInfo
        commune = CommuneInfo.objects.only("logo").first()
        if commune and commune.logo:
            return {"site_logo": commune.logo, "site_logo_url": commune.logo.url}
    except Exception:
        pass
    return {"site_logo": None, "site_logo_url": None}
