import datetime
import json
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponse
from core.models import ReservationCentreLoisirs, LeisureCenter, LeisureDayStatus
from core.permissions import user_is_centre_loisirs_admin
from core.email_service import send_reservation_validee_email, send_reservation_refusee_email
from core.security import require_admin_ip

def _require_cl_admin(request):
    if not user_is_centre_loisirs_admin(request.user):
        from core.views import custom_403
        return custom_403(request)
    return None

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_dashboard(request):
    if denied := _require_cl_admin(request): return denied

    today = datetime.date.today()
    attente_count = ReservationCentreLoisirs.objects.filter(statut='en_attente').count()
    resas_today = ReservationCentreLoisirs.objects.filter(date=today, statut='validee')

    # Détection de doublons (Inscriptions multiples pour un même nom/prénom)
    from core.models import InscriptionCentreLoisirs
    doublons_qs = (
        InscriptionCentreLoisirs.objects.values('nom_enfant', 'prenom_enfant')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )
    doublons = [f"{d['prenom_enfant']} {d['nom_enfant']}" for d in doublons_qs]

    return render(request, 'panel/centre_loisirs/dashboard.html', {
        'attente_count': attente_count,
        'resas_today': resas_today,
        'doublons': doublons,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_reservations(request):
    if denied := _require_cl_admin(request): return denied

    reservations = ReservationCentreLoisirs.objects.filter(statut='en_attente').select_related('inscription').order_by('inscription__created_at', 'date')

    return render(request, 'panel/centre_loisirs/reservations.html', {
        'reservations': reservations,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_valider_reservation(request, pk):
    if denied := _require_cl_admin(request): return denied
    if request.method == 'POST':
        resa = get_object_or_404(ReservationCentreLoisirs, pk=pk)
        message_personnalise = request.POST.get('message_personnalise')
        resa.statut = 'validee'
        resa.date_validation = datetime.datetime.now()
        resa.validee_par = request.user
        resa.save()
        send_reservation_validee_email(resa, request, message_personnalise)
        messages.success(request, f"Réservation de {resa.inscription.prenom_enfant} validée.")
    return redirect('admin_cl_reservations')

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_refuser_reservation(request, pk):
    if denied := _require_cl_admin(request): return denied
    if request.method == 'POST':
        resa = get_object_or_404(ReservationCentreLoisirs, pk=pk)
        motif = request.POST.get('motif', 'Capacité maximale atteinte')
        resa.statut = 'refusee'
        resa.motif_refus = motif
        resa.date_validation = datetime.datetime.now()
        resa.validee_par = request.user
        resa.save()
        send_reservation_refusee_email(resa, motif)
        messages.warning(request, f"Réservation de {resa.inscription.prenom_enfant} refusée.")
    return redirect('admin_cl_reservations')

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_supprimer_reservation(request, pk):
    if denied := _require_cl_admin(request): return denied
    if request.method == 'POST':
        resa = get_object_or_404(ReservationCentreLoisirs, pk=pk)
        resa.delete()
        messages.info(request, "Réservation supprimée.")
    return redirect('admin_cl_reservations')

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_gestion_jours(request):
    if denied := _require_cl_admin(request): return denied
    centre = LeisureCenter.objects.first()

    if request.method == 'POST':
        action_type = request.POST.get('action_type', 'multi_dates')

        if action_type == 'multi_dates':
            dates_json = request.POST.get('dates_json', '[]')
            status = request.POST.get('status', 'ouvert')
            motif = request.POST.get('motif', '')
            try:
                dates_list = json.loads(dates_json)
                count_added = 0
                for date_str in dates_list:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    LeisureDayStatus.objects.update_or_create(
                        centre=centre,
                        date=date_obj,
                        defaults={'status': status, 'motif_fermeture': motif}
                    )
                    count_added += 1
                if count_added > 0:
                    label = "ouvert(s)" if status == 'ouvert' else "fermé(s)"
                    messages.success(request, f"{count_added} jour(s) enregistré(s) comme {label}.")
                else:
                    messages.warning(request, "Aucune date sélectionnée.")
            except (json.JSONDecodeError, ValueError) as e:
                messages.error(request, f"Erreur dans les dates : {e}")

        elif action_type == 'supprimer':
            jour_id = request.POST.get('jour_id')
            try:
                LeisureDayStatus.objects.filter(pk=jour_id, centre=centre).delete()
                messages.info(request, "Exception supprimée.")
            except Exception as e:
                messages.error(request, f"Erreur : {e}")

        return redirect('admin_cl_gestion_jours')

    jours = LeisureDayStatus.objects.filter(centre=centre).order_by('-date')[:200]

    # Préparer les données JSON pour le calendrier interactif JS
    jours_data = {}
    for jour in LeisureDayStatus.objects.filter(centre=centre):
        jours_data[jour.date.strftime('%Y-%m-%d')] = {
            'status': jour.status,
            'motif': jour.motif_fermeture,
        }

    return render(request, 'panel/centre_loisirs/gestion_jours.html', {
        'jours': jours,
        'jours_json': json.dumps(jours_data),
    })

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_historique(request):
    if denied := _require_cl_admin(request): return denied

    if request.method == 'POST':
        resa_id = request.POST.get('resa_id')
        new_status = request.POST.get('new_status')
        if resa_id and new_status in ['validee', 'refusee', 'annulee', 'en_attente']:
            try:
                resa = ReservationCentreLoisirs.objects.get(pk=resa_id)
                resa.statut = new_status
                resa.save()
                messages.success(request, f"Statut de la réservation mis à jour : {new_status}")
            except ReservationCentreLoisirs.DoesNotExist:
                messages.error(request, "Réservation introuvable.")
        return redirect(request.get_full_path())

    reservations = ReservationCentreLoisirs.objects.all().select_related('inscription')

    date_filter = request.GET.get('date')
    enfant_filter = request.GET.get('enfant')
    parent_filter = request.GET.get('parent')
    statut_filter = request.GET.get('statut')
    type_filter = request.GET.get('type')

    if date_filter:
        reservations = reservations.filter(date=date_filter)
    if enfant_filter:
        reservations = reservations.filter(
            Q(inscription__prenom_enfant__icontains=enfant_filter) |
            Q(inscription__nom_enfant__icontains=enfant_filter)
        )
    if parent_filter:
        reservations = reservations.filter(
            Q(inscription__nom_responsable_1__icontains=parent_filter) |
            Q(inscription__prenom_responsable_1__icontains=parent_filter) |
            Q(inscription__nom_responsable_2__icontains=parent_filter)
        )
    if statut_filter:
        reservations = reservations.filter(statut=statut_filter)

    if type_filter == 'mercredi':
        reservations = reservations.filter(date__iso_week_day=3)
    elif type_filter == 'vacances':
        reservations = reservations.exclude(date__iso_week_day=3)

    reservations = reservations.order_by('-date', 'inscription__nom_enfant')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="historique_reservations.csv"'
        response.write(u'\ufeff'.encode('utf8'))  # BOM for Excel
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['Date', 'Enfant', 'Âge', 'Responsable', 'Téléphone', 'Email', 'Statut', 'Motif (si refus)'])
        for r in reservations:
            writer.writerow([
                r.date.strftime('%d/%m/%Y'),
                f"{r.inscription.prenom_enfant} {r.inscription.nom_enfant}",
                r.inscription.age,
                f"{r.inscription.prenom_responsable_1} {r.inscription.nom_responsable_1}",
                r.inscription.portable_1 or r.inscription.telephone_1,
                r.inscription.email_1,
                r.get_statut_display(),
                r.motif_refus if r.statut == 'refusee' else ''
            ])
        return response

    return render(request, 'panel/centre_loisirs/historique.html', {
        'reservations': reservations,
        'filters': request.GET,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_detail_jour(request, date):
    if denied := _require_cl_admin(request): return denied

    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    reservations = ReservationCentreLoisirs.objects.filter(date=date_obj, statut='validee').select_related('inscription')

    enfant_filter = request.GET.get('enfant')
    parent_filter = request.GET.get('parent')
    age_filter = request.GET.get('age')
    type_filter = request.GET.get('type')

    if enfant_filter:
        reservations = reservations.filter(
            Q(inscription__prenom_enfant__icontains=enfant_filter) |
            Q(inscription__nom_enfant__icontains=enfant_filter)
        )
    if parent_filter:
        reservations = reservations.filter(
            Q(inscription__nom_responsable_1__icontains=parent_filter) |
            Q(inscription__prenom_responsable_1__icontains=parent_filter) |
            Q(inscription__nom_responsable_2__icontains=parent_filter)
        )
    if type_filter == 'mercredi':
        reservations = reservations.filter(date__iso_week_day=3)
    elif type_filter == 'vacances':
        reservations = reservations.exclude(date__iso_week_day=3)

    if age_filter:
        try:
            age_target = int(age_filter)
            reservations = [r for r in reservations if r.inscription.age == age_target]
        except ValueError:
            pass

    for r in reservations:
        r.is_ado = r.inscription.age >= 11

    return render(request, 'panel/centre_loisirs/detail_jour.html', {
        'date': date_obj,
        'reservations': reservations,
        'filters': request.GET,
    })

@require_admin_ip
@login_required(login_url='login_admin')
def admin_cl_calendrier(request):
    if denied := _require_cl_admin(request): return denied

    # Récupérer le nombre de réservations validées par jour pour le calendrier
    counts = ReservationCentreLoisirs.objects.filter(statut='validee').values('date').annotate(total=Count('id'))
    events = []
    for c in counts:
        events.append({
            'title': f"{c['total']} inscrit(s)",
            'start': c['date'].strftime('%Y-%m-%d'),
            'url': f"/control-panel/centre-loisirs/jours/{c['date'].strftime('%Y-%m-%d')}/",
            'backgroundColor': '#10b981',  # emerald-500
            'borderColor': '#059669',
        })

    jours_fermes = LeisureDayStatus.objects.filter(status='ferme')
    for jf in jours_fermes:
        events.append({
            'title': f"Fermé{' — ' + jf.motif_fermeture if jf.motif_fermeture else ''}",
            'start': jf.date.strftime('%Y-%m-%d'),
            'backgroundColor': '#ef4444',  # red-500
            'borderColor': '#dc2626',
            'display': 'background',
        })

    jours_ouverts = LeisureDayStatus.objects.filter(status='ouvert')
    for jo in jours_ouverts:
        events.append({
            'title': f"Ouvert{' — ' + jo.motif_fermeture if jo.motif_fermeture else ''}",
            'start': jo.date.strftime('%Y-%m-%d'),
            'backgroundColor': '#f59e0b',  # amber-500
            'borderColor': '#d97706',
            'display': 'background',
        })

    return render(request, 'panel/centre_loisirs/calendrier.html', {
        'events_json': json.dumps(events)
    })
