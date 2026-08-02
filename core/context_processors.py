"""
Context processor – logo du site

Injecte automatiquement la variable `site_logo` dans tous les templates.
Si un logo est uploade dans CommuneInfo, il est utilise ; sinon None (fallback vers le statique).
"""


def site_logo(request):
    """Rend le logo de la commune disponible dans tous les templates."""
    try:
        from core.models import CommuneInfo
        commune = CommuneInfo.objects.only("logo").first()
        if commune and commune.logo:
            return {"site_logo": commune.logo}
    except Exception:
        pass
    return {"site_logo": None}
