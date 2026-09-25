import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from core.models import Signalement, SignalementPhoto, News


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

def serviceworker_js(request):
    js_content = """
const CACHE_NAME = 'dhuizon-pwa-v1';
const urlsToCache = [
  '/app/',
  '/static/images/logo-dhuizon.webp'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});
"""
    return HttpResponse(js_content, content_type="application/javascript")

def app_home(request):
    alertes = News.objects.filter(is_published=True).order_by('-created_at')[:5]
    return render(request, 'app_mobile/accueil.html', {'alertes': alertes})

def app_signalement(request):
    if request.method == 'POST':
        categorie = request.POST.get('categorie')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        adresse = request.POST.get('adresse_approximative')
        email = request.POST.get('email_signalant')

        sig = Signalement.objects.create(
            categorie=categorie,
            description=description,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None,
            adresse_approximative=adresse,
            email_signalant=email
        )

        # Handle photos (up to 5)
        for f in request.FILES.getlist('photos')[:5]:
            SignalementPhoto.objects.create(signalement=sig, image=f)

        return redirect('app_signalement_success')

    categories = Signalement.Categorie.choices
    return render(request, 'app_mobile/signalement_form.html', {'categories': categories})

def app_signalement_success(request):
    return render(request, 'app_mobile/signalement_success.html')

def app_alertes(request):
    alertes = News.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'app_mobile/alertes.html', {'alertes': alertes})

def app_pratique(request):
    return render(request, 'app_mobile/pratique.html')
