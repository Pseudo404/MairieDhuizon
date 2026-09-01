import logging
from functools import wraps
from django.conf import settings
from django.shortcuts import render

logger = logging.getLogger(__name__)

def get_client_ip(request):
    if getattr(settings, 'TRUST_X_FORWARDED_FOR', False):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR') or ''

def _localhost_ips():
    return {'127.0.0.1', '::1'}

def get_admin_allowed_ips_from_db():
    from core.models import AdminAllowedIP
    return {ip.strip() for ip in AdminAllowedIP.objects.filter(is_active=True).values_list('ip_address', flat=True) if ip}

def get_admin_fallback_ips():
    """liste IP "de secours" (settings.py -> .env)"""
    raw = getattr(settings, 'ADMIN_FALLBACK_IPS', '') or ''
    if isinstance(raw, (list, tuple)):
        return {str(ip).strip() for ip in raw if ip}
    return {ip.strip() for ip in str(raw).split(',') if ip.strip()}

def is_admin_access_allowed(request):
    """determine si accès oui ou non"""
    if not getattr(settings, 'ADMIN_IP_RESTRICTION_ENABLED', True):
        return True

    client_ip = get_client_ip(request)
    if not client_ip:
        return False # Impossible de vérifier l'IP, on bloque par sécurité

    db_ips = get_admin_allowed_ips_from_db()
    fallback_ips = get_admin_fallback_ips()
    allowed = db_ips | fallback_ips

    if allowed and client_ip in allowed:
        return True

    if settings.DEBUG and getattr(settings, 'ADMIN_ALLOW_LOCALHOST_IN_DEBUG', True):
        if client_ip in _localhost_ips():
            return True
            
    return False

def require_admin_ip(view_func):
    """decorateur @require_admin_ip -> si ip est pas accepté alors directement redirect avant d'ouvrir la page admin 403"""
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not is_admin_access_allowed(request):
            client_ip = get_client_ip(request)
            logger.warning(
                'Accès refusé à %s pour IP %s (User-Agent: %s)',
                request.path,
                client_ip,
                request.META.get('HTTP_USER_AGENT', '')[:100]
            )
            return render(
                request,
                '403_admin_ip.html',
                {'client_ip': client_ip},
                status=403,
            )
        return view_func(request, *args, **kwargs)
    return wrapped
