import json
import csv
import datetime
from datetime import timedelta
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Count, Avg
from django.db.models.functions import TruncHour
from django.apps import apps
from django.forms import modelform_factory
from core.models import (AgencePostale, CabaneCocou, ChildcareProfessional, CommuneInfo,Commerce, CommerceSchedule, Entreprise, GlassCollectionPoint, HealthCenter,Gite, HealthcareProfessional, Hebergement, LeisureCenter, LieuTouristique,Mediatheque, MenuCantine, MunicipalCouncilReport,MunicipalCouncilor, News, NextCouncilMeeting, Nursery, PatrimoineItem, Pharmacy, QuickLink,CommuneMedia, HistoireDhuizon, RecyclingCenter, School, SeniorResidence,SportFacility, TextileCollectionPoint, Transport, WasteCollectionSchedule, PageView,DemarcheAdministrative, Randonnee)
from core.forms import ContactForm, NewsForm, AdminLoginForm, AdminAccountForm, InscriptionPeriscolaireForm
from core.email_service import send_contact_email, send_confirmation_email, send_periscolaire_email
from core.uploads import file_response_for_path
from core.security import require_admin_ip
from core.permissions import user_is_super_admin, user_is_panel_admin
from core.opening_hours import (build_annuaire_horaires, current_recycling_season, evaluate_weekly_schedules, season_label, today_weekday_key, WEEKDAY_LABELS)
from core.recherche import rechercher
from django_ratelimit.decorators import ratelimit

@ensure_csrf_cookie
@ratelimit(key='ip', rate='30/m', block=True)
def home(request):
    all_news = News.objects.filter(is_published=True)
    quick_links = QuickLink.objects.all()
    gallery = CommuneMedia.objects.all()
    hero_image = CommuneMedia.objects.filter(is_hero=True).first()
    return render(request, 'accueil.html', {
        'all_news': all_news,
        'quick_links': quick_links,
        'gallery': gallery,
        'hero_image': hero_image,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def decouvrir_dhuizon(request):
    communeinfo = CommuneInfo.objects.first()
    hero_image = CommuneMedia.objects.filter(is_hero=True).first()
    histoire = HistoireDhuizon.objects.all()
    patrimoine = PatrimoineItem.objects.all()
    return render(request, 'decouvrir-dhuizon.html', {
        'communeinfo': communeinfo,
        'hero_image': hero_image,
        'histoire': histoire,
        'patrimoine': patrimoine,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def loisirs(request):
    sport_infos = SportFacility.objects.select_related('type_equipement').all()
    randonnees = Randonnee.objects.all()
    return render(request, 'loisirs.html', {
        'sports': sport_infos,
        'randonnees': randonnees,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def randonnee_detail(request, slug):
    randonnee = get_object_or_404(Randonnee, slug=slug)
    return render(request, 'randonnee_detail.html', {
        'randonnee': randonnee,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def tourisme(request):
    hero_image = CommuneMedia.objects.filter(is_hero_tourisme=True).first()
    lieux = LieuTouristique.objects.all()
    cabanes = CabaneCocou.objects.all()
    hebergements = Hebergement.objects.all()
    gites = Gite.objects.all()
    return render(request, 'tourisme.html', {
        'hero_image': hero_image,
        'lieux': lieux,
        'cabanes': cabanes,
        'hebergements': hebergements,
        'gites': gites,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def entreprises(request):
    commerces = Commerce.objects.prefetch_related('horaires').all()
    entreprises_qs = Entreprise.objects.prefetch_related('horaires').all()
    return render(request, 'entreprises.html', {
        'page_badge': 'Économie locale',
        'page_icon': 'domain',
        'page_title': 'Entreprises & Commerces',
        'page_intro': (
            "Retrouvez ici les commerces et entreprises de la commune de Dhuizon. "
            "Cliquez sur une ligne pour afficher les horaires d'ouverture."
        ),
        'annuaire_sections': [
            {
                'id': 'commerces',
                'title': 'Commerces',
                'icon': 'store',
                'data': build_annuaire_horaires(commerces),
                'empty_title': 'Aucun commerce enregistré',
                'empty_message': (
                    "L'annuaire des commerces sera bientôt disponible.<br>"
                    "Les informations sont ajoutées depuis le panneau d'administration."
                ),
                'empty_icon': 'store',
            },
            {
                'id': 'entreprises',
                'title': 'Entreprises',
                'icon': 'domain',
                'data': build_annuaire_horaires(entreprises_qs),
                'empty_title': 'Aucune entreprise enregistrée',
                'empty_message': (
                    "L'annuaire des entreprises sera bientôt disponible.<br>"
                    "Les informations sont ajoutées depuis le panneau d'administration."
                ),
                'empty_icon': 'domain',
            },
        ],
    })

@ratelimit(key='ip', rate='30/m', block=True)
def vie_pratique(request):
    school_info = School.objects.first()
    health_center_info = HealthCenter.objects.first()
    pharmacy_info = Pharmacy.objects.first()
    senior_center_info = SeniorResidence.objects.first()
    dechets_info = WasteCollectionSchedule.objects.all()
    decheterie_info = RecyclingCenter.objects.first()
    mediatheque_info = Mediatheque.objects.first()
    nursery_info = Nursery.objects.first()
    centres_loisirs = LeisureCenter.objects.first()
    assistantes_mat = ChildcareProfessional.objects.all()
    points_verre = GlassCollectionPoint.objects.all()
    points_textiles = TextileCollectionPoint.objects.all()
    transports = Transport.objects.all()
    agence_postale = AgencePostale.objects.first()
    commune_info = CommuneInfo.objects.first()

    today_label = WEEKDAY_LABELS.get(today_weekday_key(), '')
    decheterie_saison = current_recycling_season()

    def get_schedule(info_obj, horaires_attr='horaires_planning', season=None):
        if not info_obj:
            return False, 'Informations non disponibles', []
        horaires = getattr(info_obj, horaires_attr).all()
        if season:
            return evaluate_weekly_schedules(horaires, season=season)
        return evaluate_weekly_schedules(horaires)

    pharmacy_open, pharmacy_status, pharmacy_today_slots = get_schedule(pharmacy_info)
    senior_open, senior_status, senior_today_slots = get_schedule(senior_center_info)
    decheterie_open, decheterie_status, decheterie_today_slots = get_schedule(
        decheterie_info, horaires_attr='horaires', season=decheterie_saison
    )

    health_professionals = []
    if health_center_info:
        health_professionals = health_center_info.professionnels.order_by('order', 'profession', 'nom', 'prenom')

    commune_open, commune_status, commune_today_slots = get_schedule(commune_info)
    mediatheque_open, mediatheque_status, mediatheque_today_slots = get_schedule(mediatheque_info)
    agence_postale_open, agence_postale_status, agence_postale_today_slots = get_schedule(agence_postale)

    import datetime
    now = datetime.datetime.now()
    week_number = now.isocalendar()[1]
    is_even_week = (week_number % 2 == 0)
    
    if is_even_week:
        semaine_type = "paire"
        poubelle_semaine = "jaune"
    else:
        semaine_type = "impaire"
        poubelle_semaine = "verte"

    # ── Menu cantine ──────────────────────────────────────────────────────────
    today = now.date()
    current_year = today.isocalendar()[0]
    week_number = today.isocalendar()[1]
    
    menus_semaine = []
    plat_du_jour = None
    try:
        # On récupère tous les menus de la semaine actuelle
        menus = MenuCantine.objects.filter(annee=current_year, numero_semaine=week_number)
        menus_semaine = list(menus)
        
        # On trie la liste en python par jour (Lundi -> Vendredi)
        jour_order = {"lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4, "vendredi": 5}
        menus_semaine.sort(key=lambda m: jour_order.get(m.jour, 99))
        
        # Plat du jour (uniquement en semaine, lundi=0 … vendredi=4)
        jour_key_map = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi"}
        jour_today_key = jour_key_map.get(today.weekday())
        if jour_today_key:
            plat_du_jour = next(
                (m for m in menus_semaine if m.jour == jour_today_key), None
            )
    except Exception as e:
        # Table pas encore migrée ou autre erreur DB
        menus_semaine = []
        plat_du_jour = None

    return render(request, 'vie_pratiques.html', {
        'school': school_info,
        'health_center': health_center_info,
        'health_professionals': health_professionals,
        'pharmacy': pharmacy_info,
        'pharmacy_open': pharmacy_open,
        'pharmacy_status': pharmacy_status,
        'pharmacy_today_slots': pharmacy_today_slots,
        'senior_center': senior_center_info,
        'senior_open': senior_open,
        'senior_status': senior_status,
        'senior_today_slots': senior_today_slots,
        'dechets': dechets_info,
        'decheterie': decheterie_info,
        'decheterie_open': decheterie_open,
        'decheterie_status': decheterie_status,
        'decheterie_today_slots': decheterie_today_slots,
        'decheterie_saison': decheterie_saison,
        'decheterie_saison_label': season_label(decheterie_saison),
        'today_label': today_label,
        'mediatheque': mediatheque_info,
        'mediatheque_open': mediatheque_open,
        'mediatheque_status': mediatheque_status,
        'mediatheque_today_slots': mediatheque_today_slots,
        'nursery': nursery_info,
        'centres_loisirs': centres_loisirs,
        'assistantes_mat': assistantes_mat,
        'points_verre': points_verre,
        'points_textiles': points_textiles,
        'transports': transports,
        'commune_info': commune_info,
        'commune_open': commune_open,
        'commune_status': commune_status,
        'commune_today_slots': commune_today_slots,
        'agence_postale': agence_postale,
        'agence_postale_open': agence_postale_open,
        'agence_postale_status': agence_postale_status,
        'agence_postale_today_slots': agence_postale_today_slots,
        'week_number': week_number,
        'semaine_type': semaine_type,
        'poubelle_semaine': poubelle_semaine,
        'menus_semaine': menus_semaine,
        'plat_du_jour': plat_du_jour,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def actualite_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id, is_published=True)
    return render(request, 'actualite_detail.html', {
        'news_item': news_item
    })

@ratelimit(key='ip', rate='5/m', block=True)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            success, error_msg = send_contact_email(
                nom=data['nom'],
                prenom=data['prenom'],
                email=data['email'],
                telephone=data.get('telephone', ''),
                objet=data['objet'],
                message=data['message'],
            )
            if success:
                send_confirmation_email(data['email'], data['prenom'])
                messages.success(
                    request,
                    "Votre message a bien été envoyé ! Nous vous répondrons dans les meilleurs délais."
                )
                return redirect('contact')
            else:
                messages.error(request, error_msg)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        initial = {}
        if request.GET.get('objet'):
            initial['objet'] = request.GET['objet']
        if request.GET.get('message'):
            initial['message'] = request.GET['message']
        form = ContactForm(initial=initial)
    return render(request, 'contact.html', {'form': form})

@ratelimit(key='ip', rate='30/m', block=True)
def conseil_municipal(request):
    all_conseil = MunicipalCouncilReport.objects.all().order_by('-date')
    conseillers = MunicipalCouncilor.objects.filter(is_conseil_jeunes=False)
    conseil_jeunes = MunicipalCouncilor.objects.filter(is_conseil_jeunes=True)
    prochain_conseil = NextCouncilMeeting.objects.first()
    return render(request, 'conseil_municipal.html', {
        'all_conseil': all_conseil,
        'conseillers': conseillers,
        'conseil_jeunes': conseil_jeunes,
        'prochain_conseil': prochain_conseil,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def vie_associative(request):
    from core.models import Association
    associations = Association.objects.all().order_by('nom')
    return render(request, 'vie_associative.html', {
        'associations': associations,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def association_detail(request, slug):
    from core.models import Association
    asso = get_object_or_404(Association, slug=slug)
    return render(request, 'association_detail.html', {
        'asso': asso,
    })

@ratelimit(key='ip', rate='30/m', block=True)
def demarches(request):
    return redirect('/vie-pratique/#demarches')

@ratelimit(key='ip', rate='30/m', block=True)
def etat_civil(request):
    return render(request, 'etat_civil.html')

@ratelimit(key='ip', rate='60/m', block=True)
def vue_recherche(request):
    q = request.GET.get("q", "").strip()
    resultats = rechercher(q)
    return render(request, "recherche.html", {"resultats": resultats, "q": q})

@ratelimit(key='ip', rate='60/m', block=True)
def serve_upload(request, relative_path):
    """fichiers (PDF, images)"""
    return file_response_for_path(relative_path)

@require_admin_ip
@ratelimit(key='ip', rate='4/m', block=True)
def login_admin(request):
    from core.permissions import user_is_only_centre_loisirs_admin, user_is_panel_admin
    
    if request.user.is_authenticated and request.user.is_staff:
        if user_is_only_centre_loisirs_admin(request.user):
            return redirect('admin_cl_dashboard')
        return redirect('control_panel')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Bienvenue, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)
                if user_is_only_centre_loisirs_admin(user):
                    return redirect('admin_cl_dashboard')
                return redirect('control_panel')
            else:
                messages.error(request, "Vous n'avez pas les droits d'accès administrateur.")
    else:
        form = AdminLoginForm()
    
    return render(request, 'login_admin.html', {'form': form})

@require_admin_ip
@login_required(login_url='login_admin')
def logout_admin(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('home')

@require_admin_ip
@login_required(login_url='login_admin')
@ratelimit(key='ip', rate='10/m', block=True)
def control_panel(request):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    today = timezone.now().date()
    views_today = PageView.objects.filter(created_at__date=today).count()
    return render(request, 'control_panel.html', {
        'views_today': views_today,
    })

@require_admin_ip
@login_required(login_url='login_admin')
@ratelimit(key='ip', rate='10/m', block=True)
def admin_settings(request):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    from core.panel import SETTINGS_MENU
    menu = []
    for group_title, items in SETTINGS_MENU:
        group_items = []
        for t, d, i, url_name, kwargs in items:
            opts = dict(kwargs)
            if opts.pop('super_admin_only', False) and not user_is_super_admin(request.user):
                continue
            group_items.append({
                'title': t, 'description': d, 'icon': i,
                'url': reverse(url_name, kwargs=opts) if opts else reverse(url_name),
            })
        if group_items:
            menu.append({'title': group_title, 'items': group_items})
    return render(request, 'panel/settings.html', {'settings_groups': menu})

@require_admin_ip
@login_required(login_url='login_admin')
@ratelimit(key='user', rate='120/m', block=True)
def admin_stats(request):
    if not user_is_panel_admin(request.user):
        return custom_403(request)

    now = timezone.now()
    today = now.date()
    first_day_of_month = today.replace(day=1)

    if today.month == 1:
        first_day_prev_month = today.replace(year=today.year - 1, month=12, day=1)
    else:
        first_day_prev_month = today.replace(month=today.month - 1, day=1)

    views_today = PageView.objects.filter(created_at__date=today).count()
    views_month = PageView.objects.filter(created_at__date__gte=first_day_of_month).count()
    views_prev_month = PageView.objects.filter(
        created_at__date__gte=first_day_prev_month,
        created_at__date__lt=first_day_of_month
    ).count()

    unique_today = PageView.objects.filter(
        created_at__date=today
    ).values('session_key').distinct().count()
    unique_month = PageView.objects.filter(
        created_at__date__gte=first_day_of_month
    ).values('session_key').distinct().count()

    avg_time_result = PageView.objects.filter(
        time_on_page__isnull=False, time_on_page__gt=0, time_on_page__lt=3600,
    ).aggregate(avg=Avg('time_on_page'))
    avg_time = round(avg_time_result['avg'] or 0)

    if views_prev_month > 0:
        growth = round(((views_month - views_prev_month) / views_prev_month) * 100, 1)
    else:
        growth = 100.0 if views_month > 0 else 0.0

    thirty_days_ago = today - timedelta(days=29)
    daily_views = (
        PageView.objects
        .filter(created_at__date__gte=thirty_days_ago)
        .values('created_at__date')
        .annotate(count=Count('id'))
        .order_by('created_at__date')
    )
    daily_data = {e['created_at__date']: e['count'] for e in daily_views}

    daily_unique = (
        PageView.objects
        .filter(created_at__date__gte=thirty_days_ago)
        .values('created_at__date')
        .annotate(count=Count('session_key', distinct=True))
        .order_by('created_at__date')
    )
    daily_unique_data = {e['created_at__date']: e['count'] for e in daily_unique}

    chart_labels, chart_data, chart_unique_data = [], [], []
    for i in range(30):
        day = thirty_days_ago + timedelta(days=i)
        chart_labels.append(day.strftime('%d/%m'))
        chart_data.append(daily_data.get(day, 0))
        chart_unique_data.append(daily_unique_data.get(day, 0))

    hourly_views = (
        PageView.objects
        .filter(created_at__date=today)
        .annotate(hour=TruncHour('created_at'))
        .values('hour')
        .annotate(count=Count('id'))
        .order_by('hour')
    )
    hourly_data = {}
    for e in hourly_views:
        h = e['hour']
        if h is not None:
            hourly_data[h.hour] = e['count']
    hourly_labels = [f'{h:02d}h' for h in range(24)]
    hourly_counts = [hourly_data.get(h, 0) for h in range(24)]

    top_pages = PageView.objects.values('path').annotate(count=Count('id')).order_by('-count')[:10]

    countries = [
        {'country': (e['country'] or 'Inconnu'), 'count': e['count']}
        for e in PageView.objects.values('country').annotate(count=Count('id')).order_by('-count')[:10]
    ]

    browsers = list(PageView.objects.exclude(browser='').values('browser').annotate(count=Count('id')).order_by('-count'))

    devices = list(PageView.objects.values('device_type').annotate(count=Count('id')).order_by('-count'))

    five_min_ago = now - timedelta(minutes=5)
    realtime_count = PageView.objects.filter(created_at__gte=five_min_ago).values('session_key').distinct().count()

    total_views = PageView.objects.count()

    context = {
        'views_today': views_today,
        'views_month': views_month,
        'unique_today': unique_today,
        'unique_month': unique_month,
        'avg_time': avg_time,
        'growth': growth,
        'total_views': total_views,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'chart_unique_data': chart_unique_data,
        'hourly_labels': hourly_labels,
        'hourly_counts': hourly_counts,
        'top_pages': top_pages,
        'countries_json': countries,
        'browsers_json': browsers,
        'devices_json': devices,
        'realtime_count': realtime_count,
    }
    return render(request, 'panel/stats.html', context)

@require_admin_ip
@login_required(login_url='login_admin')
@ratelimit(key='user', rate='10/h', block=True)
def api_realtime_count(request):
    if not user_is_panel_admin(request.user):
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    five_min_ago = timezone.now() - timedelta(minutes=5)
    count = PageView.objects.filter(created_at__gte=five_min_ago).values('session_key').distinct().count()
    return JsonResponse({'count': count})

@require_POST
@ratelimit(key='ip', rate='30/m', block=True)
def api_track_time(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST uniquement'}, status=405)
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'JSON invalide'}, status=400)

    session_key = getattr(request.session, 'session_key', None)
    time_spent = data.get('time', 0)
    path = data.get('path', '')

    if session_key and isinstance(time_spent, (int, float)) and time_spent > 0 and path:
        time_spent = min(int(time_spent), 3600)
        pv = PageView.objects.filter(session_key=session_key, path=path).order_by('-created_at').first()
        if pv and pv.time_on_page is None:
            pv.time_on_page = time_spent
            pv.save(update_fields=['time_on_page'])
    return JsonResponse({'ok': True})

@require_admin_ip
@login_required(login_url='login_admin')
@ratelimit(key='user', rate='5/h', block=True)
def api_export_csv(request):
    if not user_is_panel_admin(request.user):
        return HttpResponse(status=403)

    today = timezone.now().date()
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="statistiques_dhuizon_{today}.csv"'
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Date', 'Heure', 'Page', 'Navigateur', 'Appareil', 'Temps (s)'])
    for pv in PageView.objects.all().order_by('-created_at'):
        writer.writerow([
            pv.created_at.strftime('%d/%m/%Y'),
            pv.created_at.strftime('%H:%M:%S'),
            pv.path, pv.browser,
            pv.device_type, pv.time_on_page if pv.time_on_page is not None else '',
        ])
    return response

def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception=None):
    return render(request, '403.html', status=403)

def politique_confidentialite(request):
    return render(request, 'politique_confidentialite.html')

def ratelimited_error(request, exception=None):
    return render(request, 'ratelimited.html', status=429)

def too_many_requests(request):
    return render(request, 'ratelimited.html', status=429)

@login_required(login_url='login_admin')
def admin_audit_logs(request):
    if not user_is_panel_admin(request.user):
        return custom_403(request)

    from django.utils import timezone
    from datetime import timedelta
    from core.models import AuditLog

    three_months_ago = timezone.now() - timedelta(days=90)
    logs_qs = AuditLog.objects.select_related('user').filter(created_at__gte=three_months_ago)

    action_filter = request.GET.get('action')
    if action_filter:
        logs_qs = logs_qs.filter(action=action_filter)

    user_filter = request.GET.get('user')
    if user_filter:
        logs_qs = logs_qs.filter(user__username=user_filter)

    from django.core.paginator import Paginator
    paginator = Paginator(logs_qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Liste des utilisateurs pour le filtre
    from django.contrib.auth.models import User
    users = User.objects.filter(audit_logs__isnull=False).distinct()

    return render(request, 'panel/logs.html', {
        'page_obj': page_obj,
        'action_filter': action_filter,
        'user_filter': user_filter,
        'users': users,
        'actions': AuditLog.Action.choices,
    })

SINGLETON_MODELS = [
    'communeinfo', 'school', 'healthcenter', 'pharmacy',
    'seniorresidence', 'nursery', 'mediatheque', 'recyclingcenter',
    'agencepostale', 'leisurecenter', 'nextcouncilmeeting'
]

def _require_super_admin(request):
    if not user_is_super_admin(request.user):
        return custom_403(request)
    return None

def _admin_account_protected(instance, request):
    """Comptes Super Admin non modifiables depuis le panel."""
    if instance.is_super_admin:
        messages.error(request, "Les comptes Super Admin ne peuvent pas être modifiés depuis ce panneau.")
        return True
    if instance.user_id == request.user.id:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        return True
    return False

@require_admin_ip
@login_required(login_url='login_admin')
def panel_crud_list(request, app_label, model_name):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    if model_name.lower() == 'adminaccount':
        denied = _require_super_admin(request)
        if denied:
            return denied
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404("Modèle introuvable")
    
    if model_name.lower() in SINGLETON_MODELS:
        instance = model.objects.first()
        if instance:
            return redirect('panel_crud_edit', app_label=app_label, model_name=model_name, pk=instance.pk)
        else:
            return redirect('panel_crud_add', app_label=app_label, model_name=model_name)
    
    objects = model.objects.all()
    
    parent_model = None
    parent_filter = None
    if model_name.lower() == 'commerceschedule':
        parent_model = apps.get_model(app_label, 'commerce')
        parent_filter = 'commerce_id'
    elif model_name.lower() == 'entrepriseschedule':
        parent_model = apps.get_model(app_label, 'entreprise')
        parent_filter = 'entreprise_id'
        
    parent_instance = None
    if parent_model:
        parent_id = request.GET.get('parent_id')
        if not parent_id:
            parents = parent_model.objects.all()
            if hasattr(parent_model, 'order'):
                parents = parents.order_by('order')
            return render(request, 'panel/crud_select_parent.html', {
                'model_name': model._meta.verbose_name.title() if hasattr(model._meta, 'verbose_name') else model_name,
                'model_name_plural': model._meta.verbose_name_plural.title() if hasattr(model._meta, 'verbose_name_plural') else model_name + "s",
                'app_label': app_label,
                'model_slug': model_name,
                'parents': parents,
            })
        else:
            objects = objects.filter(**{parent_filter: parent_id})
            parent_instance = parent_model.objects.get(pk=parent_id)

    if hasattr(model, 'order'):
        objects = objects.order_by('order')
    elif model._meta.ordering:
        objects = objects.order_by(*model._meta.ordering)
    elif hasattr(model, 'created_at'):
        objects = objects.order_by('-created_at')
        
    import datetime
    return render(request, 'panel/crud_list.html', {
        'model_name': model._meta.verbose_name.title() if hasattr(model._meta, 'verbose_name') else model_name,
        'model_name_plural': model._meta.verbose_name_plural.title() if hasattr(model._meta, 'verbose_name_plural') else model_name + "s",
        'app_label': app_label,
        'model_slug': model_name,
        'objects': objects,
        'parent_instance': parent_instance,
        'is_admin_accounts': model_name.lower() == 'adminaccount',
        'current_user_is_super_admin': user_is_super_admin(request.user),
        'current_week': datetime.date.today().isocalendar()[1] if model_name.lower() == 'menucantine' else None,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def panel_crud_form(request, app_label, model_name, pk=None):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    if model_name.lower() == 'adminaccount':
        denied = _require_super_admin(request)
        if denied:
            return denied
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404("Modèle introuvable")
        
    instance = get_object_or_404(model, pk=pk) if pk else None

    if model_name.lower() == 'adminaccount' and instance and instance.is_super_admin:
        messages.error(request, "Les comptes Super Admin ne peuvent pas être modifiés depuis ce panneau.")
        return redirect('panel_crud_list', app_label=app_label, model_name=model_name)
    
    if model_name.lower() == 'quicklink':
        from core.forms import QuickLinkForm
        FormClass = QuickLinkForm
    elif model_name.lower() == 'news':
        from core.forms import NewsForm
        FormClass = NewsForm
    elif model_name.lower() == 'adminaccount':
        FormClass = AdminAccountForm
    else:
        FormClass = modelform_factory(model, exclude=['created_at', 'updated_at'])
    
    is_singleton = model_name.lower() in SINGLETON_MODELS

    initial = {}
    parent_id = request.GET.get('parent_id')
    if parent_id and not pk:
        if model_name.lower() == 'commerceschedule':
            initial['commerce'] = parent_id
        elif model_name.lower() == 'entrepriseschedule':
            initial['entreprise'] = parent_id

    if request.method == 'POST':
        if model_name.lower() == 'adminaccount':
            form = FormClass(request.POST, admin_account=instance)
        else:
            form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Enregistrement réussi.")
            if is_singleton:
                return redirect('admin_settings')
            redirect_url = reverse('panel_crud_list', kwargs={'app_label': app_label, 'model_name': model_name})
            if parent_id:
                redirect_url += f"?parent_id={parent_id}"
            return redirect(redirect_url)
    else:
        if model_name.lower() == 'adminaccount':
            form = FormClass(admin_account=instance, initial=initial)
        else:
            form = FormClass(instance=instance, initial=initial)
        
    import datetime
    return render(request, 'panel/crud_form.html', {
        'form': form,
        'model_name': model._meta.verbose_name.title() if hasattr(model._meta, 'verbose_name') else model_name,
        'app_label': app_label,
        'model_slug': model_name,
        'is_edit': bool(pk),
        'instance': instance,
        'is_singleton': is_singleton,
        'parent_id': parent_id,
        'current_week': datetime.date.today().isocalendar()[1] if model_name.lower() == 'menucantine' else None,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def panel_crud_delete(request, app_label, model_name, pk):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    if model_name.lower() == 'adminaccount':
        denied = _require_super_admin(request)
        if denied:
            return denied
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404("Modèle introuvable")
        
    instance = get_object_or_404(model, pk=pk)

    if model_name.lower() == 'adminaccount' and _admin_account_protected(instance, request):
        return redirect('panel_crud_list', app_label=app_label, model_name=model_name)
    
    if request.method == 'POST':
        if model_name.lower() == 'adminaccount':
            instance.user.delete()
        else:
            instance.delete()
        messages.success(request, f"Suppression réussie.")
        parent_id = request.GET.get('parent_id')
        redirect_url = reverse('panel_crud_list', kwargs={'app_label': app_label, 'model_name': model_name})
        if parent_id:
            redirect_url += f"?parent_id={parent_id}"
        return redirect(redirect_url)
        
    return render(request, 'panel/crud_delete.html', {
        'model_name': model._meta.verbose_name.title() if hasattr(model._meta, 'verbose_name') else model_name,
        'app_label': app_label,
        'model_slug': model_name,
        'instance': instance,
    })

@require_admin_ip
@login_required(login_url='login_admin')
@require_POST
def panel_crud_toggle_publish(request, app_label, model_name, pk):
    if not user_is_panel_admin(request.user):
        return custom_403(request)
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        raise Http404("Modèle introuvable")
        
    instance = get_object_or_404(model, pk=pk)
    
    if hasattr(instance, 'is_published'):
        instance.is_published = not instance.is_published
        instance.save(update_fields=['is_published'])
        status_msg = "publié" if instance.is_published else "dépublié"
        messages.success(request, f"L'élément a été {status_msg} avec succès.")
    else:
        messages.error(request, "Cet élément n'a pas de statut de publication.")
        
    return redirect('panel_crud_list', app_label=app_label, model_name=model_name)


@ratelimit(key='ip', rate='10/m', block=True)
def inscription_periscolaire(request):
    """
    Formulaire d'inscription périscolaire (Garderie / Cantine).
    Envoie les données par email à la mairie via Brevo.
    """
    # Plus de préremplissage avec un service unique puisque c'est une grille
    initial = {}

    import datetime
    now = datetime.datetime.now()
    if now.month < 7:
        annee_scolaire = f"{now.year - 1}-{now.year}"
    else:
        annee_scolaire = f"{now.year}-{now.year + 1}"


    if request.method == 'POST':
        form = InscriptionPeriscolaireForm(request.POST)
        if form.is_valid():
            success, error_msg = send_periscolaire_email(form.cleaned_data)
            if success:
                messages.success(
                    request,
                    "Votre demande d'inscription a bien été envoyée ! "
                    "Vous allez recevoir un accusé de réception par email."
                )
                return redirect('inscription_periscolaire')
            else:
                messages.error(
                    request,
                    error_msg or "Une erreur est survenue lors de l'envoi. Veuillez réessayer."
                )
    else:
        form = InscriptionPeriscolaireForm(initial=initial)

    from core.models import PeriscolaireInfo
    periscolaire_info = PeriscolaireInfo.objects.first()

    return render(request, 'inscription_periscolaire.html', {'form': form, 'annee_scolaire': annee_scolaire, 'periscolaire_info': periscolaire_info})
