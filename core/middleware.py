"""
Middlewares personnalisés pour l'application core.

Un middleware est un composant de Django qui s'exécute silencieusement à chaque 
requête (entrante) et réponse (sortante). Ce fichier contient :
1. Une protection de l'accès à l'interface d'administration.
2. Un système de suivi (tracking) des visites des utilisateurs.
"""
import re
import logging
from django.conf import settings
from django.shortcuts import render
from core.security import get_client_ip, is_admin_access_allowed

logger = logging.getLogger(__name__)

EXCLUDED_PATHS = [
    re.compile(r'^/admin/'),
    re.compile(r'^/assets/'),
    re.compile(r'^/media/'),
    re.compile(r'^/api/'),
    re.compile(r'^/__reload__/'),
    re.compile(r'^/favicon'),
    re.compile(r'^/control-panel/'),
]

BOT_PATTERNS = [
    'bot', 'spider', 'crawl', 'slurp', 'baiduspider',
    'googlebot', 'bingbot', 'yandexbot', 'duckduckbot',
    'facebookexternalhit', 'twitterbot', 'linkedinbot',
    'whatsapp', 'telegrambot', 'headlesschrome', 'python-requests',
    'curl', 'wget', 'httpclient', 'libwww-perl', 'scrapy',
]

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/admin/') and not is_admin_access_allowed(request):
            client_ip = get_client_ip(request)
            logger.warning('Accès /admin/ refusé pour IP %s', client_ip)
            return render(request, '403_admin_ip.html', {'client_ip': client_ip}, status=403)
        return self.get_response(request)

class PageViewTrackingMiddleware:
    """
    Système d'analytics (statistiques) interne très léger.
    Il enregistre chaque page HTML visitée en base de données, 
    en excluant les requêtes techniques et les visites de robots.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != 'GET' or response.status_code != 200:
            return response

        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        path = request.path

        for pattern in EXCLUDED_PATHS:
            if pattern.match(path):
                return response

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ua_lower = user_agent.lower()
        if any(bot in ua_lower for bot in BOT_PATTERNS):
            return response

        if not request.session.session_key:
            request.session.create()

        browser = self._parse_browser(ua_lower)
        device_type = self._parse_device(ua_lower)

        referer = request.META.get('HTTP_REFERER', '')
        if referer and len(referer) > 200:
            referer = referer[:200]
        referer = referer or None

        try:
            from core.models import PageView
            PageView.objects.create(
                path=path,
                user_agent=user_agent[:500],
                browser=browser,
                device_type=device_type,
                referer=referer,
                session_key=request.session.session_key or '',
            )
        except Exception as e:
            logger.error(f"Erreur lors du tracking de la visite: {e}")
        return response

    @staticmethod
    def _parse_browser(ua_lower):
        if 'edg' in ua_lower:
            return 'Edge'
        elif 'opr' in ua_lower or 'opera' in ua_lower:
            return 'Opera'
        elif 'chrome' in ua_lower and 'safari' in ua_lower:
            return 'Chrome'
        elif 'firefox' in ua_lower:
            return 'Firefox'
        elif 'safari' in ua_lower:
            return 'Safari'
        elif 'msie' in ua_lower or 'trident' in ua_lower:
            return 'IE'
        return 'Autre'

    @staticmethod
    def _parse_device(ua_lower):
        if any(kw in ua_lower for kw in ['ipad', 'tablet', 'kindle', 'silk']):
            return 'tablet'
        elif any(kw in ua_lower for kw in ['mobile', 'iphone']):
            return 'mobile'
        elif 'android' in ua_lower and 'mobile' not in ua_lower:
            return 'tablet'
        elif 'android' in ua_lower:
            return 'mobile'
        return 'desktop'
