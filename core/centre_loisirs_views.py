import datetime
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django_ratelimit.decorators import ratelimit
from core.models import LeisureCenter, InscriptionCentreLoisirs, ReservationCentreLoisirs, LeisureDayStatus
from core.forms import InscriptionCentreLoisirsForm
from core.email_service import send_reservation_demande_email, send_reservation_annulee_email
import calendar
from django.db.models import Count, Q

def get_jour_statut(date_obj, centre):
    feries = [
        (1, 1), (5, 1), (5, 8), (7, 14), (8, 15), (11, 1), (11, 11), (12, 25)
    ]
    if (date_obj.month, date_obj.day) in feries:
        return 'ferie'

    status = LeisureDayStatus.objects.filter(centre=centre, date=date_obj).first()
    if status:
        if status.status == 'ouvert':
            if centre:
                resa_validees = ReservationCentreLoisirs.objects.filter(date=date_obj, statut='validee').count()
                if resa_validees >= centre.capacite_max:
                    return 'complet'
            return 'ouvert'
        return status.status

    return 'ferme'

@ratelimit(key='ip', rate='30/m', block=True)
def centre_loisirs_choix_dates(request):
    """Étape 1 : page de sélection des dates (calendrier visuel)."""
    return render(request, 'centre_loisirs/choix_dates.html')

@ratelimit(key='ip', rate='30/m', block=True)
def centre_loisirs_formulaire(request):
    """Étape 2 : formulaire d'inscription + traitement POST."""
    centre = LeisureCenter.objects.first()
    if request.method == 'POST':
        form = InscriptionCentreLoisirsForm(request.POST, request.FILES)
        dates_str = request.POST.getlist('dates')
        dates = []
        
        for d in dates_str:
            try:
                date_obj = datetime.datetime.strptime(d, '%Y-%m-%d').date()
                statut = get_jour_statut(date_obj, centre)
                if statut == 'ouvert' and date_obj >= datetime.date.today():
                    dates.append(date_obj)
            except ValueError:
                pass
                
        if not dates:
            messages.error(request, "Veuillez sélectionner au moins une date valide sur le calendrier.")
            return render(request, 'centre_loisirs/inscription.html', {'form': form, 'centre': centre})

        if form.is_valid():
            justificatif = request.FILES.get('justificatif_quotient_familial')
            livret = request.FILES.get('livret_famille_doc')
            jugement = request.FILES.get('jugement_familial')
            identite = request.FILES.get('personnes_habilitees_identite')

            inscriptions_creees = []
            resas_creees_global = []

            MAX_ENFANTS = 10
            enfant_indices = sorted({
                int(key.rsplit('_', 1)[1])
                for key in request.POST
                if key.startswith('nom_enfant_') and key.rsplit('_', 1)[1].isdigit()
            })[:MAX_ENFANTS]
            for i in enfant_indices:
                nom_enfant = request.POST.get(f'nom_enfant_{i}')
                prenom_enfant = request.POST.get(f'prenom_enfant_{i}')
                date_naissance = request.POST.get(f'date_naissance_{i}')
                
                if nom_enfant and prenom_enfant and date_naissance:
                    inscription = form.save(commit=False)
                    inscription.pk = None
                    inscription.token = uuid.uuid4()
                    inscription.nom_enfant = nom_enfant
                    inscription.prenom_enfant = prenom_enfant
                    inscription.date_naissance = date_naissance
                    
                    inscription.pai_sante = request.POST.get(f'pai_sante_{i}', '')
                    if f'vaccins_{i}' in request.FILES:
                        inscription.vaccins = request.FILES[f'vaccins_{i}']
                    if f'assurance_scolaire_{i}' in request.FILES:
                        inscription.assurance_scolaire = request.FILES[f'assurance_scolaire_{i}']
                        
                    inscription.justificatif_quotient_familial = justificatif
                    inscription.livret_famille_doc = livret
                    inscription.jugement_familial = jugement
                    inscription.personnes_habilitees_identite = identite

                    from django.core.exceptions import ValidationError
                    try:
                        # Force la validation du modèle (y compris les extensions de fichiers)
                        inscription.full_clean()
                    except ValidationError as e:
                        error_msgs = []
                        for field, errors in e.message_dict.items():
                            for err in errors:
                                error_msgs.append(f"{err}")
                        messages.error(request, "Erreur dans les fichiers ou les données : " + " / ".join(error_msgs))
                        return render(request, 'centre_loisirs/inscription.html', {'form': form, 'centre': centre})

                    inscription.save()
                    inscriptions_creees.append(inscription)

                    resas_creees = []
                    for d in dates:
                        resa, created = ReservationCentreLoisirs.objects.get_or_create(
                            inscription=inscription,
                            date=d,
                            defaults={'statut': 'en_attente'}
                        )
                        if created:
                            resas_creees.append(d)
                            if d not in resas_creees_global:
                                resas_creees_global.append(d)
                    
                    if resas_creees:
                        send_reservation_demande_email(inscription, resas_creees)

            if inscriptions_creees:
                return redirect('centre_loisirs_confirmation', token=inscriptions_creees[0].token)
            else:
                messages.error(request, "Veuillez renseigner les informations de l'enfant.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire d'inscription.")
    else:
        form = InscriptionCentreLoisirsForm()
        
    return render(request, 'centre_loisirs/inscription.html', {
        'form': form,
        'centre': centre
    })

@ratelimit(key='ip', rate='30/m', block=True)
def centre_loisirs_reservation(request, token):
    return redirect('centre_loisirs_inscription')

@ratelimit(key='ip', rate='30/m', block=True)
def api_calendrier_data(request):
    """
    Retourne pour chaque jour des 365 prochains jours :
      - statut : ouvert / ferme / complet / ferie
      - periode : nom de la période de vacances ou du motif (ou null)
    """
    today = datetime.date.today()
    centre = LeisureCenter.objects.first()
    
    data = {}
    for i in range(365):
        d = today + datetime.timedelta(days=i)
        statut = get_jour_statut(d, centre)
        entry = {'statut': statut}
        
        status_db = LeisureDayStatus.objects.filter(centre=centre, date=d).first()
        if status_db and status_db.motif_fermeture:
            entry['periode'] = status_db.motif_fermeture
            
        data[d.strftime('%Y-%m-%d')] = entry
        
    return JsonResponse(data)

@ratelimit(key='ip', rate='30/m', block=True)
def centre_loisirs_confirmation(request, token):
    inscription = get_object_or_404(InscriptionCentreLoisirs, token=token)
    return render(request, 'centre_loisirs/confirmation.html', {'inscription': inscription})

@ratelimit(key='ip', rate='10/m', block=True)
def centre_loisirs_annulation(request, token):
    reservation = get_object_or_404(ReservationCentreLoisirs, token_annulation=token)
    
    if request.method == 'POST':
        if reservation.date >= datetime.date.today() + datetime.timedelta(days=2):
            reservation.statut = 'annulee'
            reservation.save()
            send_reservation_annulee_email(reservation)
            messages.success(request, "La réservation a été annulée.")
        else:
            messages.error(request, "Il est trop tard pour annuler cette réservation (délai de 48h).")
        return redirect('centre_loisirs_annulation', token=token)
        
    return render(request, 'centre_loisirs/annulation.html', {'reservation': reservation})
