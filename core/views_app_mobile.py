import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
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
            {"src": logo_url, "sizes": "192x192", "type": "image/png"},
            {"src": logo_url, "sizes": "512x512", "type": "image/png"},
        ]
    }
    return JsonResponse(manifest)


def serviceworker_js(request):
    js_content = """
const CACHE_NAME = 'dhuizon-pwa-v1';
const urlsToCache = ['/app/', '/static/images/logo-dhuizon.webp'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache)));
});
self.addEventListener('fetch', event => {
  event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));
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


def app_actualite_detail(request, news_id):
    alerte = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'app_mobile/actualite_detail.html', {'alerte': alerte})


def _get_pratique_context():
    from core.models import (School, Pharmacy, SeniorResidence, RecyclingCenter,
                              WasteCollectionSchedule, Mediatheque, CommuneInfo,
                              LeisureCenter, GlassCollectionPoint, TextileCollectionPoint,
                              AgencePostale, MenuCantine)
    from core.views import (evaluate_weekly_schedules, today_weekday_key,
                             WEEKDAY_LABELS, current_recycling_season, season_label)
    import datetime

    now = datetime.datetime.now()
    today = now.date()
    week_number = today.isocalendar()[1]
    current_year = today.isocalendar()[0]
    is_even_week = (week_number % 2 == 0)
    semaine_type = "paire" if is_even_week else "impaire"
    poubelle_semaine = "jaune" if is_even_week else "verte"
    decheterie_saison = current_recycling_season()

    def get_schedule(info_obj, horaires_attr='horaires_planning', season=None):
        if not info_obj:
            return False, 'Informations non disponibles', []
        horaires = getattr(info_obj, horaires_attr).all()
        if season:
            return evaluate_weekly_schedules(horaires, season=season)
        return evaluate_weekly_schedules(horaires)

    school = School.objects.first()
    pharmacy = Pharmacy.objects.first()
    senior_center = SeniorResidence.objects.first()
    decheterie = RecyclingCenter.objects.first()
    dechets = WasteCollectionSchedule.objects.all()
    mediatheque = Mediatheque.objects.first()
    commune_info = CommuneInfo.objects.first()
    centres_loisirs = LeisureCenter.objects.first()
    points_verre = GlassCollectionPoint.objects.all()
    points_textiles = TextileCollectionPoint.objects.all()
    agence_postale = AgencePostale.objects.first()

    pharmacy_open, pharmacy_status, pharmacy_today_slots = get_schedule(pharmacy)
    senior_open, senior_status, senior_today_slots = get_schedule(senior_center)
    decheterie_open, decheterie_status, decheterie_today_slots = get_schedule(
        decheterie, horaires_attr='horaires', season=decheterie_saison)
    commune_open, commune_status, commune_today_slots = get_schedule(commune_info)
    mediatheque_open, mediatheque_status, mediatheque_today_slots = get_schedule(mediatheque)
    agence_postale_open, agence_postale_status, agence_postale_today_slots = get_schedule(agence_postale)

    try:
        menu_hebdo = MenuCantine.objects.filter(annee=current_year, numero_semaine=week_number).first()
    except Exception:
        menu_hebdo = None

    return {
        'school': school,
        'pharmacy': pharmacy,
        'pharmacy_status': pharmacy_status,
        'pharmacy_today_slots': pharmacy_today_slots,
        'senior_center': senior_center,
        'senior_status': senior_status,
        'senior_today_slots': senior_today_slots,
        'decheterie': decheterie,
        'decheterie_status': decheterie_status,
        'decheterie_today_slots': decheterie_today_slots,
        'decheterie_saison': decheterie_saison,
        'decheterie_saison_label': season_label(decheterie_saison),
        'dechets': dechets,
        'points_verre': points_verre,
        'points_textiles': points_textiles,
        'mediatheque': mediatheque,
        'mediatheque_status': mediatheque_status,
        'mediatheque_today_slots': mediatheque_today_slots,
        'commune_info': commune_info,
        'commune_status': commune_status,
        'commune_today_slots': commune_today_slots,
        'agence_postale': agence_postale,
        'agence_postale_status': agence_postale_status,
        'agence_postale_today_slots': agence_postale_today_slots,
        'centres_loisirs': centres_loisirs,
        'week_number': week_number,
        'semaine_type': semaine_type,
        'poubelle_semaine': poubelle_semaine,
        'menu_hebdo': menu_hebdo,
    }


def app_pratique(request):
    ctx = _get_pratique_context()
    return render(request, 'app_mobile/pratique.html', ctx)


def app_pratique_dechets(request):
    ctx = _get_pratique_context()
    return render(request, 'app_mobile/pratique_dechets.html', ctx)


def app_pratique_sante(request):
    ctx = _get_pratique_context()
    return render(request, 'app_mobile/pratique_sante.html', ctx)


def app_pratique_ecole(request):
    ctx = _get_pratique_context()
    return render(request, 'app_mobile/pratique_ecole.html', ctx)


def app_pratique_mairie(request):
    ctx = _get_pratique_context()
    return render(request, 'app_mobile/pratique_mairie.html', ctx)
