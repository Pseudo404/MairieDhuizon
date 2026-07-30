from django.db.models import Q
from django.db import models
from core.models import *

MOTS_CLES_MODELES = {
    "News": [
        "actualité", "actualités", "news", "article", "événement", "annonce", "information", "actualite", "evenement", "annonce", "information", "actus", "actu", "nouvelle", "nouvelles", "info", "infos"
    ],
    "Association": [
        "association", "club", "bénévolat", "volontariat", "organisation", "asso", "assos", "activités", "activité", "loisirs", "culture", "sport", "social", "solidarité"
    ],
    "School": [
        "école", "ecole", "scolaire", "collège", "lycée", "primaire", "maternelle",
        "enseignement", "éducation", "education", "classe", "élève", "eleve", "professeur",
        "prof", "enseignant", "étudiant", "etudiant", "cantine", "garderie", "périscolaire", "periscolaire", 
        "activités périscolaires", "activites periscolaires"
    ],
    "HealthCenter": [
        "médecin", "medecin", "médecine", "medecine", "santé", "sante", "méd", "med", "medcin"
        "docteur", "cabinet", "clinique", "hôpital", "hopital", "infirmier",
        "soins", "consultation", "centre de santé", "urgences", "urgence",
    ],
    "Pharmacy": [
        "pharmacie", "pharmacien", "médicament", "medicament", "ordonnance", "pharm", "pharmaciene", "médicaments", "medicaments", "médic", "medic", "pharmacie de garde", "certificat médical", "certificat medical"
    ],
    "Mediatheque": [
        "médiathèque", "mediatheque", "bibliothèque", "bibliotheque", "livre",
        "lecture", "dvd", "média", "media", "emprunter", "livre audio", "livre audio", "audiobook", "audiolivre", "revue", "magazine", "exposition", "animation", "atelier",
        "livres", "dvds", "medias", "revues", "magazines", "expositions", "animations", "ateliers",
        "mairie-médiathèque", "mairie-mediatheque", "mairie mediatheque", "mairie médiathèque", "books", "book",
    ],
    "LieuTouristique": [
        "tourisme", "touristique", "visite", "monument", "patrimoine", "musée",
        "musee", "culture", "attraction", "découverte", "découvrir", "lieu touristique", "lieu touristique", "site touristique", "site touristique",
        "a visité", "a visiter", "a-visiter", "a-visiter", "visite", "visiter", "a voir", "a-voir",
    ],
    "Commerce": [
        "commerce", "magasin", "boutique", "commerçant", "achat", "vente",
        "commerce professionnel", "commerces professionnels", "commerce de proximité", "commerce de proximite",
        "alimentaire", "restauration", "resto", "restaurant", "bar", "café", "cafe", "coiffeur",
        "esthétique", "esthetique", "auto-école", "auto-ecole", "boulanger", "boulangerie", "boucher",
        "boucherie", "fleuriste", "librairie",
    ],
    "Entreprise": [
        "entreprise", "entreprises", "société", "societe", "firme", "implantation", "économie locale",
        "economie locale", "industrie", "usine", "atelier", "siège", "siege", "bureau", "site industriel",
        "artisan", "professionnel",
    ],
    "Transport": [
        "transport", "bus", "navette", "covoiturage", "train", "mobilité",
        "mobilite", "déplacement", "deplacement", "horaire", "ligne",
        "arrêt", "arret", "gare", "station", "transports en commun", "transport en commun", "transport en commun", "bus scolaire", "navette scolaire"
    ],
    "Hotel": [
        "hébergement", "hebergement", "hôtel", "hotel", "gite", "gites", "nuit", "nuits",
        "chambre", "nuitée", "nuitee", "dormir", "logement", "séjour", "sejour", "auberge"
    ],
    "Gite": [
        "gîte", "gite", "gîtes", "gites", "location", "meublé", "meuble", "vacances"
    ],
    "AgencePostale": [
        "agence postale", "poste", "courrier", "courier", "colis", "coli", "timbre", "envoi", "retrait", "poste restante"
    ],
    "MunicipalCouncilReport": [
        "conseil municipal", "compte rendu", "deliberation", "procès verbal", "pv", "cr", "compte-rendu", "deliberation", "procès-verbal", "conseil", "municipal"
    ],
    "SportFacility": [
        "sport", "sports", "installation sportive", "terrain", "gymnase", "piscine", "stade", "salle de sport", "fitness", "tennis", "pétanque", "petanque"
    ], 
    "SeniorResidence": [
        "résidence", "residence", "logement", "aide", "aidé", "personne âgée", "senior", "vieux", "vielles",
    ],
    "Nursery": [
        "crèche", "creche", "garderie", "petite enfance", "enfant", "enfants", "accueil", "bébé", "bebe", "micro-crèche", "micro-creche", "micro creche", "micro crèche", "microcreche", "microcrèche", "petit",
    ],
    "WasteCollectionSchedule": [
        "déchets", "dechets", "collecte", "ordures", "poubelle", "tri", "recyclage",
    ],
    "RecyclingCenter": [
        "déchetterie", "dechetterie", "recyclage", "tri", "decheterie", "décheterie",
        "déchets", "dechets", "collecte", "ordures", "poubelle"
    ],
    "LeisureCenter": [
        "loisirs", "loisir", "centre de loisirs", "centre de loisir", "activité", "activiter", "activités", "activites", "jeunesse", "jeunese",
    ],
    "ChildcareProfessional": [
        "assistante maternelle", "assistante maternelle", "assistante", "assist", "assists", "maternelle", "maternel", "garde d'enfant", "garde denfant", "petite enfance", "enfant", "accueil", "petit"
    ],
    "GlassCollectionPoint": [
        "point de verre", "verre", "bouteille", "flacon", "collecte", "déchets", "dechets", "dechet", "dechets",
    ],
    "TextileCollectionPoint": [
        "point textile", "textile", "vêtement", "vetement", "collecte", "déchets", "dechets", "déchet", "dechet",
    ],
    "CabaneCocou": [
        "cabane cocou", "cocou", "cabane dans les arbres", "hébergement insolite", "hebergement insolite", "nuit insolite", "nuitée insolite", "nuitee insolite", "nuit", "nuits", "coocou", "coucou",
    ],
    "NextCouncilMeeting": [
        "prochain conseil municipal", "conseil municipal", "prochain conseil", "conseil", "municipal", "prochain", "réunion du conseil", "reunion du conseil", "réunion", "reunion",
    ],
    "MunicipalCouncilor": [
        "conseiller municipal", "membre du conseil", "conseil municipal", "municipal", "conseiller", "membre", "conseillers",
    ],
    "PeriscolaireInfo": [
        "périscolaire", "periscolaire", "inscription", "garderie", "cantine", "inscriptions", "inscription périscolaire", "inscription periscolaire", "activités périscolaires", "activites periscolaires", "activité périscolaire", "activite periscolaire", "inscription", "loisirs", "loisir", "centre de loisirs", "centre de loisir", "jeunesse", "jeunese", "enfant", "enfants", "midi", "soir", "matin", "vacances scolaires", "vacances", "vacance", "scolaire", "garderie", "cantine", "repas", "repas du midi", "repas du soir", "repas du matin", "repas du midi et du soir", "repas du midi et du matin", "repas du soir et du matin", "repas du midi, du soir et du matin", "manger"
    ]
}

PAGES_MODELES = {
    "News": {"url": "/#actualite", "label": "Actualités"},
    "Association": {"url": "/vie-associative/", "label": "Associations"},
    "School": {"url": "/vie-pratique#ecole", "label": "Écoles"},
    "HealthCenter": {"url": "/vie-pratique#sante", "label": "Santé"},
    "Pharmacy": {"url": "/vie-pratique#ouvert-maintenant", "label": "Pharmacies"},
    "Mediatheque": {"url": "/vie-pratique#mairie-mediatheque", "label": "Médiathèque"},
    "LieuTouristique": {"url": "/tourisme/", "label": "Tourisme"},
    "CabaneCocou": {"url": "/tourisme#cabanes-cocou", "label": "Cabanes Coocou"},
    "Hotel": {"url": "/tourisme#hotel", "label": "Hébergements"},
    "Gite": {"url": "/tourisme#gites", "label": "Gîtes"},
    "Commerce": {"url": "/commerces/", "label": "Commerces & Professionnels"},
    "Entreprise": {"url": "/entreprises/", "label": "Entreprises"},
    "Transport": {"url": "/vie-pratique#transports", "label": "Transports"},
    "AgencePostale": {"url": "/vie-pratique#agence-postale", "label": "Agence Postale"},
    "NextCouncilMeeting": {"url": "/conseil-municipal#prochain-conseil", "label": "Prochain conseil municipal"},
    "MunicipalCouncilReport": {"url": "/conseil-municipal#comptes-rendus", "label": "Comptes-rendus du conseil municipal"},
    "MunicipalCouncilor": {"url": "/conseil-municipal#elus", "label": "Conseillers municipaux"},
    "LeisureCenter": {"url": "/vie-pratique#jeunesse", "label": "Centre de loisirs"},
    "ChildcareProfessional": {"url": "/petite-enfance/", "label": "Assistantes maternelles"},
    "Nursery": {"url": "/vie-pratique#petite-enfance", "label": "Crèches"},
    "GlassCollectionPoint": {"url": "/vie-pratique#collecte-dechets", "label": "Points de verre"},
    "TextileCollectionPoint": {"url": "/vie-pratique#collecte-dechets", "label": "Points textiles"},
    "RecyclingCenter": {"url": "/vie-pratique#collecte-dechets", "label": "Déchetterie"},
    "WasteCollectionSchedule": {"url": "/vie-pratique#collecte-dechets", "label": "Collecte des déchets"},
    "SportFacility": {"url": "/loisirs/#sport", "label": "Installations sportives"},
    "SeniorResidence": {"url": "/vie-pratique#seniors", "label": "Résidence seniors"},
    "PeriscolaireInfo": {"url": "/inscription-periscolaire/", "label": "Inscription périscolaire"},
}

MODELES_RECHERCHE = [News, Association, School, HealthCenter, Pharmacy, Mediatheque, LieuTouristique, Nursery, WasteCollectionSchedule, RecyclingCenter, SportFacility, Commerce, Entreprise, Transport, Hebergement, Gite, AgencePostale, MunicipalCouncilor, MunicipalCouncilReport, NextCouncilMeeting, LeisureCenter, ChildcareProfessional, GlassCollectionPoint, TextileCollectionPoint, CabaneCocou, SeniorResidence, PeriscolaireInfo]

def _modele_correspond_aux_mots_cles(nom_modele: str, q: str) -> bool:
    """verifie si le mot est dans la liste pré-établie"""
    q_lower = q.lower().strip()
    mots_cles = MOTS_CLES_MODELES.get(nom_modele, [])
    for mot in mots_cles:
        if q_lower in mot or mot in q_lower:
            return True
    return False

def _construire_requete_champs(modele, q: str) -> Q:
    """verifie si le mot est présent dans une table de la bdd"""
    requete = Q()
    mots = [m for m in q.lower().strip().split() if len(m) > 1]
    champs_texte = [
        champ.name for champ in modele._meta.fields
        if isinstance(champ, (
            models.CharField,
            models.TextField,
            models.EmailField,
            models.URLField,
        ))
    ]
    for mot in mots:
        sous_requete = Q()
        for champ in champs_texte:
            sous_requete |= Q(**{f"{champ}__icontains": mot})
        requete |= sous_requete
    return requete

def _get_titre_objet(obj) -> str:
    for attr in ("nom", "title", "titre", "nom_activite", "label"):
        val = getattr(obj, attr, None) # si none pas d'erreur au lieu de obj.titre
        if val:
            return str(val)
    return str(obj)

def _get_description_objet(obj) -> str:
    """une courte description"""
    for attr in ("short_description", "description_courte", "description", "description_detaillee", "content", "presentation", "infos", "infos_complementaires", "notes", "adresse"):
        val = getattr(obj, attr, None)
        if val:
            texte = str(val)
            return texte[:150] + "…" if len(texte) > 150 else texte
    return ""

def _get_url_objet(obj, url_base: str) -> str:
    """l'URL de l'objet, sinon l'URL de liste."""
    try:
        return obj.get_absolute_url()
    except AttributeError:
        if obj.pk:
            return f"{url_base}{obj.pk}/" #primary key
        return url_base

def rechercher(q: str) -> list:
    """recherche dans les listes pré-définie et dans les tables de la bdd une correspondance"""
    if not q or len(q.strip()) < 2: # plus de deux caractère
        return []

    resultats = []
    pages_deja_ajoutees = set()

    for modele in MODELES_RECHERCHE:
        nom_modele = modele.__name__
        page_info = PAGES_MODELES.get(nom_modele, {"url": "/", "label": nom_modele})

        if _modele_correspond_aux_mots_cles(nom_modele, q):
            cle_page = page_info["url"]
            if cle_page not in pages_deja_ajoutees:
                pages_deja_ajoutees.add(cle_page)
                resultats.append({
                    "titre": page_info["label"],
                    "description": f"Rubrique correspondant à votre recherche « {q} »",
                    "url": page_info["url"],
                    "categorie": page_info["label"],
                    "source": nom_modele,
                    "type": "page",
                })

        requete = _construire_requete_champs(modele, q)
        if not requete:
            continue

        objets = modele.objects.filter(requete)[:10]

        for obj in objets:
            url_objet = _get_url_objet(obj, page_info["url"])
            resultats.append({
                "titre": _get_titre_objet(obj),
                "description": _get_description_objet(obj),
                "url": url_objet,
                "categorie": page_info["label"],
                "source": nom_modele,
                "type": "objet",
            })

    return resultats