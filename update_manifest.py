import re

with open('core/views_app_mobile.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_manifest_func = """
def manifest_json(request):
    from core.models import CommuneInfo
    commune = CommuneInfo.objects.only("logo").first()
    
    logo_url = "/static/images/logo-dhuizon.webp"
    if commune and commune.logo:
        logo_url = commune.logo.url

    manifest = {
        "name": "Mairie de Dhuizon",
        "short_name": "Dhuizon",
        "description": "L'application officielle de la Mairie de Dhuizon",
        "start_url": "/app/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#16a34a",
        "icons": [
            {
                "src": logo_url,
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": logo_url,
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    return JsonResponse(manifest)
"""

# Replace the manifest_json function
content = re.sub(
    r'def manifest_json\(request\):.*?return JsonResponse\(manifest\)',
    new_manifest_func.strip(),
    content,
    flags=re.DOTALL
)

with open('core/views_app_mobile.py', 'w', encoding='utf-8') as f:
    f.write(content)
