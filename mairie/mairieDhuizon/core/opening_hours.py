import datetime

WEEKDAY_NAMES = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

WEEKDAY_LABELS = {
    'lundi': 'Lundi',
    'mardi': 'Mardi',
    'mercredi': 'Mercredi',
    'jeudi': 'Jeudi',
    'vendredi': 'Vendredi',
    'samedi': 'Samedi',
    'dimanche': 'Dimanche',
}

def today_weekday_key():
    return WEEKDAY_NAMES[datetime.date.today().weekday()]

def current_recycling_season():
    month = datetime.date.today().month
    return 'ete' if 4 <= month <= 10 else 'hiver'

def season_label(saison):
    return 'Été' if saison == 'ete' else 'Hiver'

def evaluate_weekly_schedules(schedules, *, season=None):
    """
    Fonction utilisée pour les éléments uniques (ex: Mairie, Pharmacie unique).
    Vérifie si, à l'heure actuelle, le lieu est ouvert ou fermé selon les horaires enregistrés en BDD.
    Retourne : (is_open: bool, status: str, slots: list)
    """
    if not schedules.exists():
        return False, 'Horaires non renseignés', []
    
    qs = schedules.filter(jour=today_weekday_key())
    
    #dechetterie les horaires change en fonction de la saison
    if season:
        qs = qs.filter(saison=season)

    slots = []
    is_open = False
    now_time = datetime.datetime.now().time()

    for s in qs.order_by('heure_ouverture'):
        if s.ferme:
            slots.append({'ferme': True, 'label': 'Fermé'})
        else:
            slots.append({
                'ferme': False,
                'ouverture': s.heure_ouverture,
                'fermeture': s.heure_fermeture,
                'label': f"{s.heure_ouverture.strftime('%H:%M')} – {s.heure_fermeture.strftime('%H:%M')}",
            })
            if s.heure_ouverture <= now_time <= s.heure_fermeture:
                is_open = True

    if not slots:
        return False, "Fermé aujourd'hui", []

    status = 'Ouvert' if is_open else 'Fermé'
    return is_open, status, slots

def build_annuaire_horaires(queryset):
    """
    Fonction utilisée pour les listes (Annuaires de commerces, d'entreprises).
    Génère un dictionnaire complet contenant le statut actuel ET le tableau de la semaine.
    """
    today = today_weekday_key()
    now_time = datetime.datetime.now().time()
    annuaire_data = []

    for fiche in queryset:
        horaires_qs = list(fiche.horaires.all().order_by('jour', 'heure_ouverture'))
        horaires_par_jour = {jour: [] for jour in WEEKDAY_NAMES}
        
        #ajout des creneaux pour chaque jour de la semaine
        for h in horaires_qs:
            horaires_par_jour[h.jour].append(h)

        slots_today = horaires_par_jour[today]
        is_open = False
        statut, statut_label = 'non_renseigne', 'Non renseigné'
        if horaires_qs and slots_today:
            if all(s.ferme for s in slots_today):
                statut, statut_label = 'ferme', 'Fermé'
            else:
                is_open = any(
                    s.heure_ouverture <= now_time <= s.heure_fermeture
                    for s in slots_today if not s.ferme and s.heure_ouverture and s.heure_fermeture
                )
                statut, statut_label = ('ouvert', 'Ouvert') if is_open else ('ferme', 'Fermé')

        jours_liste = []
        for jour_key in WEEKDAY_NAMES:
            slots = horaires_par_jour[jour_key]
            
            creneaux = [
                {'heure_ouverture': s.heure_ouverture, 'heure_fermeture': s.heure_fermeture}
                for s in slots if not s.ferme and s.heure_ouverture and s.heure_fermeture
            ]
            
            jours_liste.append({
                'label': WEEKDAY_LABELS[jour_key],     # Ex: "Mardi"
                'is_today': (jour_key == today),
                'ferme': bool(slots and all(s.ferme for s in slots)),
                'non_renseigne': not slots,
                'creneaux': creneaux,                  # La liste des heures (Matin, Aprèm)
            })

        annuaire_data.append({
            'fiche': fiche,                                  # L'objet complet (Commerce/Entreprise)
            'row_id': f"{fiche._meta.model_name}-{fiche.pk}",# ID unique pour le JavaScript (ex: commerce-12)
            'is_open': is_open,
            'statut': statut,
            'statut_label': statut_label,
            'jours': jours_liste,
            'has_horaires': bool(horaires_qs),               #si false "Aucun horaire renseigné"
        })

    return annuaire_data