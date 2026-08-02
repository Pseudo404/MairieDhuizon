"""
models.py – Site de mairie Django
Architecture de base de données propre, scalable et adaptée à l'ORM Django.

Conventions :
- BaseModel abstrait pour éviter la duplication de created_at / updated_at
- Champs verbose_name sur chaque modèle et chaque champ
- Choices centralisés dans les modèles concernés
- Slugs auto-générables (à câbler dans save() ou avec django-autoslug)
- ImageField : pensez à configurer MEDIA_ROOT / MEDIA_URL dans settings.py
- FileField (PDF) : idem
- PostgreSQL : tous les types sont nativement supportés par le backend psycopg2
"""

import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse
from core.validators import validate_image_upload, validate_pdf_upload, validate_safe_link_url, validate_document_upload

class BaseModel(models.Model):
    """ Modèle de base """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BaseSchedule(BaseModel):
    """ Horaire de base """
    jour_index = models.PositiveSmallIntegerField(default=1, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        mapping = {
            "lundi": 1, "mardi": 2, "mercredi": 3, "jeudi": 4,
            "vendredi": 5, "samedi": 6, "dimanche": 7
        }
        self.jour_index = mapping.get(getattr(self, "jour", "lundi"), 1)
        super().save(*args, **kwargs)

class CommuneInfo(BaseModel):
    """ Informations de la commune """
    presentation = models.TextField(
        verbose_name="Texte de présentation de la commune",
    )
    population = models.PositiveIntegerField(
        verbose_name="Nombre d'habitants",
    )
    superficie_ha = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Superficie (hectares)",
    )
    region = models.CharField(
        max_length=100,
        default="Centre-Val de Loire",
        verbose_name="Région",
    )

    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse de la mairie",
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email de la mairie",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone de la mairie",
    )
    horaires = models.TextField(
        verbose_name="Horaires d'ouverture",
        help_text="Exemple : Lundi-Vendredi 9h-12h / 14h-17h",
    )
    logo = models.ImageField(
        upload_to="images/commune/",
        blank=True,
        null=True,
        verbose_name="Logo de la commune",
        help_text="Logo affiché dans le header du site et sur les formulaires. Laissez vide pour utiliser le logo par défaut.",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "Information commune"
        verbose_name_plural = "Informations commune"

    def __str__(self):
        return "Informations de la commune"

    def clean(self):
        """Empêche la création d'une seconde instance (pattern singleton)."""
        from django.core.exceptions import ValidationError
        if not self.pk and CommuneInfo.objects.exists():
            raise ValidationError(
                "Une seule entrée 'Informations commune' est autorisée."
            )

class CommuneInfoSchedule(BaseSchedule):
    """ Horaires des informations de la commune """
    class Weekday(models.TextChoices):
        LUNDI = "lundi", "Lundi"
        MARDI = "mardi", "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI = "jeudi", "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI = "samedi", "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    commune = models.ForeignKey(
        CommuneInfo,
        on_delete=models.CASCADE,
        related_name="horaires_planning",
        verbose_name="Mairie",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
    )

    class Meta:
        verbose_name = "Horaire mairie"
        verbose_name_plural = "Horaires mairie"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} — Mairie"

class News(BaseModel):
    """ Actualité """
    title = models.CharField(
        max_length=255,
        verbose_name="Titre",
    )
    slug = models.SlugField(
        max_length=270,
        unique=True,
        verbose_name="Slug (URL)",
        help_text="Généré automatiquement depuis le titre.",
    )
    short_description = models.TextField(
        max_length=500,
        verbose_name="Description courte",
        help_text="Résumé affiché sur la liste des actualités.",
    )
    content = models.TextField(
        verbose_name="Contenu complet",
    )
    image = models.ImageField(
        upload_to="images/actualites/",
        blank=True,
        null=True,
        verbose_name="Image principale",
        validators=[validate_image_upload],
    )
    event_date = models.DateField(
        verbose_name="Date de l'événement",
        help_text="Date à laquelle l'événement se déroule.",
    )
    author = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Auteur",
        help_text="Optionnel – nom de l'auteur de l'article.",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Publié",
    )

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["event_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-génération du slug à la création."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "/#actualite/"

class MunicipalCouncilReport(BaseModel):
    """ Compte-rendu du conseil municipal """
    titre = models.CharField(
        max_length=255,
        verbose_name="Titre",
    )
    date = models.DateField(
        verbose_name="Date du conseil",
    )
    pdf = models.FileField(
        upload_to="documents/conseils/",
        verbose_name="Fichier PDF",
        validators=[validate_pdf_upload],
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Optionnel – résumé du conseil.",
    )

    class Meta:
        verbose_name = "Compte rendu de conseil municipal"
        verbose_name_plural = "Comptes rendus de conseils municipaux"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.titre} ({self.date})"
    
    def get_absolute_url(self):
        return "/conseil-municipal#comptes-rendus"

class Association(BaseModel):
    """ Association """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'association",
    )
    slug = models.SlugField(
        max_length=270,
        unique=True,
        blank=True,
        verbose_name="Slug (URL)",
        help_text="Généré automatiquement depuis le nom.",
    )
    description = models.TextField(
        verbose_name="Description",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    site_web = models.URLField(
        blank=True,
        verbose_name="Site web",
    )
    logo = models.ImageField(
        upload_to="images/associations/",
        blank=True,
        null=True,
        verbose_name="Logo",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "Association"
        verbose_name_plural = "Associations"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        """Auto-génération du slug à la création."""
        if not self.slug:
            base_slug = slugify(self.nom)
            slug = base_slug
            n = 1
            while Association.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return "/vie-associative/{}".format(self.slug)

class School(BaseModel):
    """ École """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'école",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse postale",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    nom_directrice = models.CharField(
        max_length=150,
        verbose_name="Nom de la directrice / directeur",
    )
    nb_eleves = models.PositiveIntegerField(
        verbose_name="Nombre d'élèves",
    )
    nb_inscrits_rentree = models.PositiveIntegerField(
        verbose_name="Inscrits à la dernière rentrée",
    )
    horaires_cours = models.TextField(
        verbose_name="Horaires des cours",
        help_text="Exemple : Lun/Mar/Jeu/Ven 8h30-11h30 / 13h30-16h30",
    )

    class Meta:
        verbose_name = "École"
        verbose_name_plural = "Écoles"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#ecole-{}".format(self.pk)

class SportFacilityType(BaseModel):
    """ Type d'installation sportive """
    nom = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Type d'équipement",
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône (classe CSS ou emoji)",
        help_text="Optionnel – ex: 'fas fa-futbol' ou '⚽'",
    )

    class Meta:
        verbose_name = "Type d'équipement sportif"
        verbose_name_plural = "Types d'équipements sportifs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class SportFacility(BaseModel):
    """ Installation sportive """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'équipement",
    )
    type_equipement = models.ForeignKey(
        SportFacilityType,
        on_delete=models.PROTECT,
        related_name="equipements",
        verbose_name="Type d'équipement",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse / lieu",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude GPS",
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude GPS",
    )
    image = models.ImageField(
        upload_to="images/sports/",
        blank=True,
        null=True,
        verbose_name="Image",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "Équipement sportif"
        verbose_name_plural = "Équipements sportifs"
        ordering = ["type_equipement", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.type_equipement})"

class HealthCenter(BaseModel):
    """ Maison de santé """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )

    class Meta:
        verbose_name = "Maison de santé"
        verbose_name_plural = "Maisons de santé"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#sante-{}".format(self.pk)

class HealthcareProfessional(BaseModel):
    """ Professionnel de santé """
    centre = models.ForeignKey(
        HealthCenter,
        on_delete=models.CASCADE,
        related_name="professionnels",
        verbose_name="Maison de santé",
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    profession = models.CharField(
        max_length=150,
        verbose_name="Profession",
        help_text="Exemple : Médecin généraliste, Kinésithérapeute…",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse",
        help_text="Utile pour les praticiens hors maison de santé (ex: dentistes).",
    )
    infos_complementaires = models.TextField(
        blank=True,
        verbose_name="Informations complémentaires",
        help_text="Horaires personnalisés, secteur conventionnel, informations d'accès…",
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les professionnels sont triés par ordre croissant, puis par profession et nom.",
    )

    class Meta:
        verbose_name = "Professionnel de santé"
        verbose_name_plural = "Professionnels de santé"
        ordering = ["order", "profession", "nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom} – {self.profession}"

class Pharmacy(BaseModel):
    """ Pharmacie """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Informations complémentaires",
        help_text="Ex. : garde de nuit, fermetures exceptionnelles… Les horaires pour le statut « ouvert / fermé » se gèrent ci-dessous.",
    )

    class Meta:
        verbose_name = "Pharmacie"
        verbose_name_plural = "Pharmacies"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class PharmacySchedule(BaseSchedule):
    """ Horaires de la pharmacie """

    class Weekday(models.TextChoices):
        LUNDI = "lundi", "Lundi"
        MARDI = "mardi", "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI = "jeudi", "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI = "samedi", "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    pharmacie = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="horaires_planning",
        verbose_name="Pharmacie",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
    )

    class Meta:
        verbose_name = "Horaire pharmacie"
        verbose_name_plural = "Horaires pharmacie"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} — {self.pharmacie.nom}"

class SeniorResidence(BaseModel):
    """ Résidence pour personnes âgées """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Informations complémentaires",
        help_text="Précisions d'accueil. Les horaires pour le statut « ouvert / fermé » se gèrent ci-dessous.",
    )

    class Meta:
        verbose_name = "Résidence senior"
        verbose_name_plural = "Résidences seniors"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class SeniorResidenceSchedule(BaseSchedule):
    """ Horaires de la résidence sénior """

    class Weekday(models.TextChoices):
        LUNDI = "lundi", "Lundi"
        MARDI = "mardi", "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI = "jeudi", "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI = "samedi", "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    residence = models.ForeignKey(
        SeniorResidence,
        on_delete=models.CASCADE,
        related_name="horaires_planning",
        verbose_name="Résidence",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
    )

    class Meta:
        verbose_name = "Horaire résidence seniors"
        verbose_name_plural = "Horaires résidence seniors"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} — {self.residence.nom}"

class Nursery(BaseModel):
    """ Crèche """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        verbose_name="Horaires d'accueil",
    )

    lien = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Lien vers le site de la crèche",
        help_text="Lien vers le site de la crèche ou de la gestionnaire.",
    )

    logo = models.ImageField(
        upload_to="images/creches/",
        blank=True,
        null=True,
        verbose_name="Logo de la crèche",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "Crèche"
        verbose_name_plural = "Crèches"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#petite-enfance"

class WasteCollectionSchedule(BaseSchedule):
    """ Calendrier de collecte des déchets """

    class WasteType(models.TextChoices):
        MENAGERS       = "menagers",    "Déchets ménagers"
        RECYCLABLES    = "recyclables", "Recyclables (tri sélectif)"
        VERRE          = "verre",       "Verre"
        ENCOMBRANTS    = "encombrants", "Encombrants"
        VEGETAUX       = "vegetaux",    "Déchets verts / végétaux"
        AUTRE          = "autre",       "Autre"

    class Weekday(models.TextChoices):
        LUNDI    = "lundi",    "Lundi"
        MARDI    = "mardi",    "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI    = "jeudi",    "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI   = "samedi",   "Samedi"

    type_dechet = models.CharField(
        max_length=20,
        choices=WasteType.choices,
        verbose_name="Type de déchet",
    )
    jour = models.CharField(
        max_length=10,
        choices=Weekday.choices,
        verbose_name="Jour de collecte",
    )
    heure = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure de collecte",
        help_text="Optionnel.",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description / précisions",
    )

    class Meta:
        verbose_name = "Planning de collecte des déchets"
        verbose_name_plural = "Plannings de collecte des déchets"
        ordering = ["jour_index", "type_dechet"]
        unique_together = [("type_dechet", "jour")]

    def __str__(self):
        return f"{self.get_type_dechet_display()} – {self.get_jour_display()}"
    
    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"

class RecyclingCenter(BaseModel):
    """ Déchetterie """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )

    class Meta:
        verbose_name = "Déchetterie"
        verbose_name_plural = "Déchetteries"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"
    

class RecyclingCenterSchedule(BaseSchedule):
    """ Horaires de la déchetterie """

    class Season(models.TextChoices):
        ETE   = "ete",   "Été (01/04 → 31/10)"
        HIVER = "hiver", "Hiver (01/11 → 31/03)"

    class Weekday(models.TextChoices):
        LUNDI    = "lundi",    "Lundi"
        MARDI    = "mardi",    "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI    = "jeudi",    "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI   = "samedi",   "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    centre = models.ForeignKey(
        RecyclingCenter,
        on_delete=models.CASCADE,
        related_name="horaires",
        verbose_name="Déchetterie",
    )
    saison = models.CharField(
        max_length=10,
        choices=Season.choices,
        verbose_name="Saison",
    )
    jour = models.CharField(
        max_length=10,
        choices=Weekday.choices,
        verbose_name="Jour",
    )
    heure_ouverture = models.TimeField(
        verbose_name="Heure d'ouverture",
    )
    heure_fermeture = models.TimeField(
        verbose_name="Heure de fermeture",
    )
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
        help_text="Cocher si la déchetterie est fermée ce jour-là pour cette saison.",
    )

    class Meta:
        verbose_name = "Horaire de déchetterie"
        verbose_name_plural = "Horaires de déchetterie"
        ordering = ["centre", "saison", "jour_index"]
        unique_together = [("centre", "saison", "jour")]

    def __str__(self):
        return (
            f"{self.centre} – {self.get_saison_display()} – "
            f"{self.get_jour_display()} : "
            f"{self.heure_ouverture:%H:%M}–{self.heure_fermeture:%H:%M}"
        )

class QuickLink(BaseModel):
    """ Lien rapide """
    ICONS_CHOICES = [
        ('school', '🎓'),
        ('sports_soccer', '⚽'),
        ('local_pharmacy', '💊'),
        ('home', '🏠'),
        ('info', 'ℹ️'),
        ('restaurant', '🍽️'),
        ('room_service', '🛎️'),
        ('kebab_dining', '🍢'),
        ('local_pizza', '🍕'),
        ('partly_cloudy_day', '⛅'),
        ('sunny', '☀️'),
        ('cloud', '☁️'),
        ('rainy_snow', '🌧️'),
        ('thunderstorm', '⛈️'),
        ('rainy', '🌧️'),
        ('health_and_safety', '🩺'),
        ('health_cross', '➕'),
        ('location_on', '📍'),
        ('phone', '☎️'),
        ('email', '✉️'),
        ('people', '👥'),
        ('event', '📅'),
        ('library_books', '📚'),
        ('elderly_woman', '👵'),
        ('child_care', '👶'),
        ('recycling', '♻️'),
        ('delete', '🗑️'),
        ('medical_services', '🏥'),
        ('directions_car', '🚌'),
        ('shopping_cart', '🛒'),
        ('park', '🌳'),
        ('directions', '🗺️'),
        ('account_balance', '🏛️'),
        ('newspaper', '📰'),
        ('calendar_month', '📅'),
        ('mail', '📧'),
        ('alarm', '🕒'),
        ('pin_drop', '📍'),
        ('book_ribbon', '📚'),
        ('celebration', '🎉'),
        ('construction', '🏗️'),
        ('home_repair_service', '🔨'),
        ('forest', '🌲'),
        ('compost', '♻️'),
        ('how_to_vote', '🗳️'),
        ('diversity_3', '👥'),
        ('trophy', '🏆'),
        ('comedy_mask', '🎭'),
        ('festival', '🎪'),
        ('shield', '🛡️'),
        ('badge', '👮'),
        ('local_fire_department', '🔥'),
        ('map', '🗺️'),
        ('church', '⛪'),
        ('file_export', '📄'),
        ('assignment', '📋'),
        ('photo', '🖼️'),
        ('send', '📨'),
        ('accessibility', '♿'),
    ]
    label = models.CharField(
        max_length=100,
        verbose_name="Libellé",
        help_text="Texte affiché sous l'icône (ex: École, Sport…)",
    )
    icon = models.CharField(
        max_length=50,
        choices=ICONS_CHOICES,
        verbose_name="Icône",
        help_text="Sélectionnez une icône prédéfinie",
    )
    url = models.CharField(
        max_length=255,
        default="/",
        verbose_name="Lien (ex: /loisirs/#sport)",
        help_text="URL locale ou externe vers laquelle pointer le lien",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Raccourci infos pratiques"
        verbose_name_plural = "Raccourcis infos pratiques"
        ordering = ["order", "label"]

    def __str__(self):
        return f"{self.label} ({self.icon})"
    
    def get_icon_display(self):
        for value, label in self.ICONS_CHOICES:
            if value == self.icon:
                return label
        return self.icon

class CommuneMedia(BaseModel):
    """ Média de la commune """
    title = models.CharField(
        max_length=200,
        verbose_name="Titre / légende",
    )
    image = models.ImageField(
        upload_to="images/galerie/",
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Optionnel – description détaillée de la photo.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )
    is_hero = models.BooleanField(
        default=False,
        verbose_name="Image héro (fond accueil)",
        help_text="Cocher pour utiliser cette photo comme fond de la section principale.",
    )
    is_hero_tourisme = models.BooleanField(
        default=False,
        verbose_name="Image héro (fond tourisme)",
        help_text="Cocher pour utiliser cette photo comme fond de la page Tourisme.",
    )

    class Meta:
        verbose_name = "Photo de la commune"
        verbose_name_plural = "Photos de la commune"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

class HistoireDhuizon(BaseModel):
    """ Histoire de Dhuizon """
    date_label = models.CharField(
        max_length=100,
        verbose_name="Date / période",
        help_text="Texte affiché comme repère temporel (ex: 1000, XIXe siècle, Aujourd'hui…)",
    )
    evenement = models.TextField(
        verbose_name="Événement",
        help_text="Description de l'événement historique.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les événements sont affichés par ordre croissant.",
    )

    class Meta:
        verbose_name = "Événement historique"
        verbose_name_plural = "Événements historiques"
        ordering = ["order", "date_label"]

    def __str__(self):
        return f"{self.date_label} – {self.evenement[:50]}"

class PatrimoineItem(BaseModel):
    """ Patrimoine de Dhuizon """
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du lieu",
        help_text="Ex: Mairie, Église Saint-Pierre, Étangs…",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Texte affiché sous le nom du lieu.",
    )
    image = models.ImageField(
        upload_to="images/patrimoine/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les éléments sont affichés par ordre croissant.",
    )

    class Meta:
        verbose_name = "Élément de patrimoine"
        verbose_name_plural = "Éléments de patrimoine"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

class AdminAllowedIP(BaseModel):
    """ IP autorisée pour l'administration """
    label = models.CharField(
        max_length=120,
        verbose_name="Libellé",
        help_text="Ex. : Mairie de Dhuizon, Bureau du maire…",
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="Adresse IP",
        help_text="IPv4 ou IPv6 publique de la mairie (ex. 203.0.113.42).",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Notes",
    )

    class Meta:
        verbose_name = "IP autorisée (/admin/)"
        verbose_name_plural = "IP autorisées (/admin/)"
        ordering = ['label', 'ip_address']

    def __str__(self):
        status = 'active' if self.is_active else 'inactive'
        return f'{self.label} — {self.ip_address} ({status})'

class AdminAccount(BaseModel):
    """ Compte Administrateur """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='admin_account')
    is_super_admin = models.BooleanField(
        default=False,
        verbose_name="Est Super Admin (Mairie)",
        help_text="Les Super Admins peuvent créer et gérer d'autres administrateurs."
    )
    is_centre_loisirs = models.BooleanField(
        default=False,
        verbose_name="Est Admin Centre de Loisirs uniquement",
        help_text="Accès restreint au panneau de gestion du centre de loisirs (pas d'accès au panel général)."
    )
    can_access_centre_loisirs = models.BooleanField(
        default=False,
        verbose_name="Accès Centre de Loisirs",
        help_text="En plus de l'accès au panel général, cet admin peut aussi accéder au centre de loisirs."
    )

    class Meta:
        verbose_name = "Compte administrateur"
        verbose_name_plural = "Comptes administrateurs"
        ordering = ['user__username']

    def __str__(self):
        if self.is_super_admin:
            role = "Super Admin"
        elif self.is_centre_loisirs:
            role = "Admin Centre de Loisirs"
        elif self.can_access_centre_loisirs:
            role = "Admin + Centre de Loisirs"
        else:
            role = "Admin Classique"
        return f"{self.user.username} ({role})"

class PageView(BaseModel):
    """ Vue de page (statistique) """
    path = models.CharField(
        max_length=500,
        verbose_name="Page visitée",
    )
    country = models.CharField(
        max_length=100,
        default="France",
        verbose_name="Pays",
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent",
    )
    browser = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Navigateur",
    )
    device_type = models.CharField(
        max_length=20,
        default="desktop",
        verbose_name="Type d'appareil",
        help_text="desktop, mobile ou tablet",
    )
    referer = models.URLField(
        blank=True,
        null=True,
        verbose_name="Page d'origine",
    )
    session_key = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Clé de session",
    )
    time_on_page = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Temps sur la page (secondes)",
    )

    class Meta:
        verbose_name = "Vue de page"
        verbose_name_plural = "Vues de pages"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['path']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        return f"{self.path} — {self.created_at:%d/%m/%Y %H:%M}"

class NextCouncilMeeting(BaseModel):
    """ Prochaine réunion du conseil """
    date = models.DateField(
        verbose_name="Date du prochain conseil",
    )
    heure = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Heure",
    )
    lieu = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Lieu",
        default="Salle du conseil municipal",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Notes",
    )

    class Meta:
        verbose_name = "Prochain conseil municipal"
        verbose_name_plural = "Prochain conseil municipal"

    def __str__(self):
        return f"Prochain conseil : {self.date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pk and NextCouncilMeeting.objects.exists():
            raise ValidationError("Une seule entrée est autorisée.")
        
    def get_absolute_url(self):
        return "/conseil-municipal#prochain-conseil"

class MunicipalCouncilor(BaseModel):
    """ Conseiller municipaux """
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    role = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Rôle / fonction",
        help_text="Ex: Maire, Adjoint au maire, Conseiller municipal…",
    )
    comissions = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Commissions",
        help_text="Ex: Urbanisme, Environnement, Culture…",
    )
    photo = models.ImageField(
        upload_to="images/conseillers/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    is_conseil_jeunes = models.BooleanField(
        default=False,
        verbose_name="Conseil des jeunes",
        help_text="Cocher si ce conseiller fait partie du conseil des jeunes.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Conseiller municipal"
        verbose_name_plural = "Conseillers municipaux"
        ordering = ["order", "nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.role}"
    
    def get_absolute_url(self):
        return "/conseil-municipal#elus"

class Transport(BaseModel):
    """ Transport """

    class TransportType(models.TextChoices):
        SCOLAIRE  = "scolaire",  "Transport scolaire"
        REGULIER  = "regulier",  "Transport régulier"

    type_transport = models.CharField(
        max_length=20,
        choices=TransportType.choices,
        verbose_name="Type",
    )
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom / numéro de ligne",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Trajet, arrêts, fréquence…",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Horaires",
    )
    lien = models.URLField(
        blank=True,
        verbose_name="Lien",
        help_text="Lien vers le site de l'opérateur ou les horaires en ligne.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Transport"
        verbose_name_plural = "Transports"
        ordering = ["type_transport", "order", "nom"]

    def __str__(self):
        return f"{self.get_type_transport_display()} — {self.nom}"
    
    def get_absolute_url(self):
        return "/vie-pratique#transports"

class LeisureCenter(BaseModel):
    """ Centre de loisirs """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Horaires / informations",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    capacite_max = models.PositiveIntegerField(
        default=30,
        verbose_name="Capacité journalière maximale",
        help_text="Nombre maximum d'enfants pouvant être accueillis par jour."
    )

    class Meta:
        verbose_name = "Centre de loisirs"
        verbose_name_plural = "Centres de loisirs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#jeunesse"

class LeisureDayStatus(BaseModel):
    """ Statut d'un jour pour le centre de loisirs """
    centre = models.ForeignKey('LeisureCenter', on_delete=models.CASCADE, related_name='jours_statuts')
    date = models.DateField(verbose_name="Date")
    status = models.CharField(
        max_length=20,
        choices=[('ouvert', 'Ouvert'), ('ferme', 'Fermé'), ('ferie', 'Férié')],
        default='ouvert',
        verbose_name="Statut"
    )
    motif_fermeture = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Motif de fermeture (optionnel)"
    )

    class Meta:
        verbose_name = "Statut journalier du centre de loisirs"
        verbose_name_plural = "Statuts journaliers du centre de loisirs"
        unique_together = ('centre', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} - {self.get_status_display()}"

class InscriptionCentreLoisirs(BaseModel):
    """ Fiche d'inscription d'un enfant au centre de loisirs """
    nom_enfant = models.CharField(max_length=100, verbose_name="Nom de l'enfant")
    prenom_enfant = models.CharField(max_length=100, verbose_name="Prénom de l'enfant")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    
    nom_responsable_1 = models.CharField(max_length=100, verbose_name="Nom (Responsable 1)")
    prenom_responsable_1 = models.CharField(max_length=100, verbose_name="Prénom (Responsable 1)")
    adresse_responsable_1 = models.CharField(max_length=255, verbose_name="Adresse (Responsable 1)")
    code_postal_1 = models.CharField(max_length=20, verbose_name="Code postal (Responsable 1)")
    ville_1 = models.CharField(max_length=100, verbose_name="Ville (Responsable 1)")
    telephone_1 = models.CharField(max_length=20, blank=True, verbose_name="Téléphone (Responsable 1)")
    portable_1 = models.CharField(max_length=20, verbose_name="Portable (Responsable 1)")
    email_1 = models.EmailField(verbose_name="Email (Responsable 1)")

    nom_responsable_2 = models.CharField(max_length=100, blank=True, verbose_name="Nom (Responsable 2)")
    prenom_responsable_2 = models.CharField(max_length=100, blank=True, verbose_name="Prénom (Responsable 2)")
    adresse_responsable_2 = models.CharField(max_length=255, blank=True, verbose_name="Adresse (Responsable 2)")
    code_postal_2 = models.CharField(max_length=20, blank=True, verbose_name="Code postal (Responsable 2)")
    ville_2 = models.CharField(max_length=100, blank=True, verbose_name="Ville (Responsable 2)")
    telephone_2 = models.CharField(max_length=20, blank=True, verbose_name="Téléphone (Responsable 2)")
    portable_2 = models.CharField(max_length=20, blank=True, verbose_name="Portable (Responsable 2)")
    email_2 = models.EmailField(blank=True, verbose_name="Email (Responsable 2)")

    coefficient_familial = models.CharField(max_length=50, blank=True, verbose_name="Coefficient familial")
    justificatif_quotient_familial = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Justificatif quotient familial")
    
    livret_famille = models.BooleanField(default=False, verbose_name="Livret de famille fourni (Ancien)")
    livret_famille_doc = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Livret de famille (Document)")
    jugement_familial = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Jugement familial")
    personnes_habilitees_identite = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Pièce d'identité (Personnes habilitées)")
    personnes_habilitees_texte = models.TextField(blank=True, verbose_name="Personnes habilitées à venir chercher l'enfant")
    
    pai_sante = models.TextField(blank=True, verbose_name="PAI informations de santé (lunettes, fauteuil, etc.)")
    vaccins = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Vaccins")
    assurance_scolaire = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload], blank=True, null=True, verbose_name="Assurance extra-scolaire")

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = "Inscription au centre de loisirs"
        verbose_name_plural = "Inscriptions au centre de loisirs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prenom_enfant} {self.nom_enfant}"

    @property
    def age(self):
        import datetime
        today = datetime.date.today()
        return today.year - self.date_naissance.year - ((today.month, today.day) < (self.date_naissance.month, self.date_naissance.day))

class ReservationCentreLoisirs(BaseModel):
    """ Une réservation pour un jour donné """
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    inscription = models.ForeignKey('InscriptionCentreLoisirs', on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField(verbose_name="Date réservée")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    token_annulation = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation/refus")
    validee_par = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations_validees')
    motif_refus = models.CharField(max_length=255, blank=True, verbose_name="Motif de refus")

    class Meta:
        verbose_name = "Réservation centre de loisirs"
        verbose_name_plural = "Réservations centre de loisirs"
        unique_together = ('inscription', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.inscription} - {self.date.strftime('%d/%m/%Y')} ({self.get_statut_display()})"

class ChildcareProfessional(BaseModel):
    """ Nourisses """
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    places_disponibles = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Places disponibles",
    )
    infos = models.TextField(
        blank=True,
        verbose_name="Informations",
    )

    class Meta:
        verbose_name = "Assistante maternelle"
        verbose_name_plural = "Assistantes maternelles"
        ordering = ["nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def get_absolute_url(self):
        return "/vie-pratique#petite-enfance"

class GlassCollectionPoint(BaseModel):
    """ Point de collecte du verre """
    nom = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nom / libellé",
        help_text="Ex: Parking de la Mairie, Rue de la Forêt…",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description / précisions",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Point de collecte du verre"
        verbose_name_plural = "Points de collecte du verre"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom or self.adresse
    
    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"

class TextileCollectionPoint(BaseModel):
    """ Point de collecte des textiles """
    nom = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Nom / libellé",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description / précisions",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Point de collecte de textiles"
        verbose_name_plural = "Points de collecte de textiles"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom or self.adresse
    
    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"

class Mediatheque(BaseModel):
    """ Médiathèque """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
        default="Médiathèque de Dhuizon",
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Horaires d'ouverture",
    )
    infos = models.TextField(
        blank=True,
        verbose_name="Informations complémentaires",
    )

    class Meta:
        verbose_name = "Médiathèque"
        verbose_name_plural = "Médiathèque"

    def __str__(self):
        return self.nom

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pk and Mediatheque.objects.exists():
            raise ValidationError("Une seule entrée médiathèque est autorisée.")
        
    def get_absolute_url(self):
        return "/vie-pratique#mairie-mediatheque"

class MediathequeSchedule(BaseSchedule):
    """ Horaires de la médiathèque """
    class Weekday(models.TextChoices):
        LUNDI = "lundi", "Lundi"
        MARDI = "mardi", "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI = "jeudi", "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI = "samedi", "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    mediatheque = models.ForeignKey(
        Mediatheque,
        on_delete=models.CASCADE,
        related_name="horaires_planning",
        verbose_name="Médiathèque",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
    )

    class Meta:
        verbose_name = "Horaire médiathèque"
        verbose_name_plural = "Horaires médiathèque"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} — {self.mediatheque.nom}"

class LieuTouristique(BaseModel):
    """ Lieu touristique """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du lieu",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    temps_trajet = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Temps de trajet",
        help_text="Ex : 15 min en voiture, 30 min à vélo…",
    )
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name="Distance (km)",
    )
    lien = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Lien vers le site officiel",
    )
    image = models.ImageField(
        upload_to="images/tourisme/lieux/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Lieu touristique"
        verbose_name_plural = "Lieux touristiques"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/tourisme#a-visiter"

class CabaneCocou(BaseModel):
    """ Cabane Cocou """
    class Statut(models.TextChoices):
        EN_PROJET      = "en_projet",      "🔜 En projet"
        EN_CONSTRUCTION = "en_construction", "🚧 En construction"
        OUVERT         = "ouvert",         "✅ Ouvert"

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de la cabane",
    )
    description = models.TextField(
        verbose_name="Description",
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_PROJET,
        verbose_name="Statut",
    )
    capacite = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Capacité (personnes)",
    )
    tarif = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Tarif indicatif",
        help_text="Ex : À partir de 120€/nuit",
    )
    lien = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Lien de réservation / site",
    )
    image = models.ImageField(
        upload_to="images/tourisme/cabanes/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Cabane Coocou"
        verbose_name_plural = "Cabanes Coocou"
        ordering = ["order", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.get_statut_display()})"
    
    def get_absolute_url(self):
        return "/tourisme#cabanes-cocou"

class Hebergement(BaseModel):
    """ Hébergement """
    class TypeHebergement(models.TextChoices):
        AUBERGE = "auberge", "Auberge"
        HOTEL   = "hotel",   "Hôtel"
        GITE    = "gite",    "Gîte"
        CAMPING = "camping", "Camping"
        AUTRE   = "autre",   "Autre"

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'hébergement",
    )
    type_hebergement = models.CharField(
        max_length=20,
        choices=TypeHebergement.choices,
        default=TypeHebergement.AUBERGE,
        verbose_name="Type",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    site_web = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Site web",
    )
    image = models.ImageField(
        upload_to="images/tourisme/hebergements/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Hébergement"
        verbose_name_plural = "Hébergements"
        ordering = ["order", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.get_type_hebergement_display()})"
    
    def get_absolute_url(self):
        return "/tourisme#hebergements"

class Gite(BaseModel):
    """ Gîte """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du gîte",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    site_web = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Site web",
    )
    capacite = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Capacité (personnes)",
    )
    tarif = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tarif indicatif",
        help_text="Ex : À partir de 80 € / nuit",
    )
    image = models.ImageField(
        upload_to="images/tourisme/gites/",
        blank=True,
        null=True,
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Gîte"
        verbose_name_plural = "Gîtes"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return "/tourisme#gites"

class Commerce(BaseModel):
    """ Commerce """
    nom_activite = models.CharField(
        max_length=255,
        verbose_name="Nom de l'activité",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    personnel = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Personnel / Responsable",
        help_text="Nom(s) du ou des responsables / gérants.",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Commerce"
        verbose_name_plural = "Commerces"
        ordering = ["order", "nom_activite"]

    def __str__(self):
        return self.nom_activite
    
    def get_absolute_url(self):
        return "/commerces/"

class CommerceSchedule(BaseSchedule):
    """ Horaires des commerces """
    class Weekday(models.TextChoices):
        LUNDI    = "lundi",    "Lundi"
        MARDI    = "mardi",    "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI    = "jeudi",    "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI   = "samedi",   "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    commerce = models.ForeignKey(
        Commerce,
        on_delete=models.CASCADE,
        related_name="horaires",
        verbose_name="Commerce",
    )
    jour = models.CharField(
        max_length=10,
        choices=Weekday.choices,
        verbose_name="Jour",
    )
    heure_ouverture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure d'ouverture",
        help_text="Laisser vide si fermé toute la journée.",
    )
    heure_fermeture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure de fermeture",
        help_text="Laisser vide si fermé toute la journée.",
    )
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
        help_text="Cocher si le commerce est fermé ce jour-là.",
    )

    class Meta:
        verbose_name = "Horaire commerce"
        verbose_name_plural = "Horaires commerce"
        ordering = ["commerce", "jour_index", "heure_ouverture"]

    def __str__(self):
        if self.ferme:
            return f"{self.get_jour_display()} — {self.commerce.nom_activite} : Fermé"
        if self.heure_ouverture and self.heure_fermeture:
            return (
                f"{self.get_jour_display()} — {self.commerce.nom_activite} : "
                f"{self.heure_ouverture:%H:%M}–{self.heure_fermeture:%H:%M}"
            )
        return f"{self.get_jour_display()} — {self.commerce.nom_activite} : Non renseigné"

class Entreprise(BaseModel):
    """ Entreprises """
    nom_activite = models.CharField(
        max_length=255,
        verbose_name="Nom de l'activité",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    personnel = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Personnel / Responsable",
        help_text="Nom(s) du ou des responsables / gérants.",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ["order", "nom_activite"]

    def __str__(self):
        return self.nom_activite

    def get_absolute_url(self):
        return "/entreprises/"

class EntrepriseSchedule(BaseSchedule):
    """ Horaires des entreprises """

    class Weekday(models.TextChoices):
        LUNDI    = "lundi",    "Lundi"
        MARDI    = "mardi",    "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI    = "jeudi",    "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI   = "samedi",   "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name="horaires",
        verbose_name="Entreprise",
    )
    jour = models.CharField(
        max_length=10,
        choices=Weekday.choices,
        verbose_name="Jour",
    )
    heure_ouverture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure d'ouverture",
        help_text="Laisser vide si fermé toute la journée.",
    )
    heure_fermeture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure de fermeture",
        help_text="Laisser vide si fermé toute la journée.",
    )
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
        help_text="Cocher si l'entreprise est fermée ce jour-là.",
    )

    class Meta:
        verbose_name = "Horaire entreprise"
        verbose_name_plural = "Horaires entreprise"
        ordering = ["entreprise", "jour_index", "heure_ouverture"]

    def __str__(self):
        if self.ferme:
            return f"{self.get_jour_display()} — {self.entreprise.nom_activite} : Fermé"
        if self.heure_ouverture and self.heure_fermeture:
            return (
                f"{self.get_jour_display()} — {self.entreprise.nom_activite} : "
                f"{self.heure_ouverture:%H:%M}–{self.heure_fermeture:%H:%M}"
            )
        return f"{self.get_jour_display()} — {self.entreprise.nom_activite} : Non renseigné"

class AgencePostale(BaseModel):
    """ Agence postale """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
        default="Agence Postale de Dhuizon",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Téléphone",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Horaires d'ouverture",
        help_text="Exemple : Lun/Mar/Jeu/Ven 9h-12h",
    )

    class Meta:
        verbose_name = "Agence postale"
        verbose_name_plural = "Agences postales"

    def __str__(self):
        return self.nom

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pk and AgencePostale.objects.exists():
            raise ValidationError("Une seule entrée agence postale est autorisée.")
        
    def get_absolute_url(self):
        return "/vie-pratique#agence-postale"

class AgencePostaleSchedule(BaseSchedule):
    """ Horaires de l'agence postale """
    class Weekday(models.TextChoices):
        LUNDI = "lundi", "Lundi"
        MARDI = "mardi", "Mardi"
        MERCREDI = "mercredi", "Mercredi"
        JEUDI = "jeudi", "Jeudi"
        VENDREDI = "vendredi", "Vendredi"
        SAMEDI = "samedi", "Samedi"
        DIMANCHE = "dimanche", "Dimanche"

    agence_postale = models.ForeignKey(
        AgencePostale,
        on_delete=models.CASCADE,
        related_name="horaires_planning",
        verbose_name="Agence postale",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="Fermé ce jour",
    )

    class Meta:
        verbose_name = "Horaire agence postale"
        verbose_name_plural = "Horaires agence postale"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} — {self.agence_postale.nom}"

class DemarcheAdministrative(BaseModel):
    """ Démarche administrative """
    titre = models.CharField(max_length=255, verbose_name="Titre de la démarche")
    description = models.TextField(verbose_name="Description / Explications", blank=True)
    lien_service_public = models.URLField(verbose_name="Lien externe (ex: service-public.fr)", blank=True)
    fichier_pdf = models.FileField(upload_to="demarches/", validators=[validate_pdf_upload], verbose_name="Fichier PDF à télécharger (ex: CERFA)", blank=True, null=True)
    icone = models.CharField(max_length=50, default="article", verbose_name="Icône Google Material", help_text="Ex: 'description', 'favorite', 'home'")
    ordre = models.PositiveSmallIntegerField(default=10, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Démarche administrative"
        verbose_name_plural = "Démarches administratives"
        ordering = ["ordre", "titre"]

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/vie-pratique/#demarches"

class AuditLog(models.Model):
    """ Journal d'audit """
    class Action(models.TextChoices):
        CREE     = "cree",      "Créé"
        MODIFIE  = "modifie",   "Modifié"
        SUPPRIME = "supprime",  "Supprimé"

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Utilisateur",
        related_name="audit_logs",
    )
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        verbose_name="Action",
    )
    section_slug = models.CharField(
        max_length=100,
        verbose_name="Section du panneau",
        help_text="Slug de la section concernée (ex : sante-professionnels)",
    )
    section_label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Libellé de la section",
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name="Modèle concerné",
        help_text="Nom du modèle Django (ex : HealthcareProfessional)",
    )
    object_pk = models.CharField(
        max_length=50,
        verbose_name="ID de l'objet",
    )
    object_repr = models.CharField(
        max_length=500,
        verbose_name="Représentation de l'objet",
        help_text="Valeur __str__ de l'objet au moment de l'action",
    )
    changes = models.TextField(
        blank=True,
        verbose_name="Détail des modifications",
        help_text="JSON : champs modifiés avec valeurs avant / après",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de l'action",
    )

    class Meta:
        verbose_name = "Log d'audit"
        verbose_name_plural = "Logs d'audit"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["user"]),
            models.Index(fields=["action"]),
            models.Index(fields=["section_slug"]),
        ]

    def __str__(self):
        user_str = self.user.get_full_name() or self.user.username if self.user else "Système"
        return f"[{self.get_action_display()}] {self.object_repr} par {user_str} — {self.created_at:%d/%m/%Y %H:%M}"

    def get_changes_display(self):
        """Désérialise le JSON des modifications pour affichage."""
        import json
        if not self.changes:
            return []
        try:
            return json.loads(self.changes)
        except (json.JSONDecodeError, ValueError):
            return []

class Randonnee(BaseModel):
    """ Randonnée """
    NIVEAU_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de la randonnée",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug (URL)",
        help_text="Généré automatiquement si laissé vide.",
    )
    description_courte = models.CharField(
        max_length=500,
        verbose_name="Description courte",
        help_text="Affichée sur la carte dans la liste des loisirs.",
    )
    description_detaillee = models.TextField(
        verbose_name="Description détaillée",
        help_text="Affichée sur la page dédiée à la randonnée.",
    )
    temps_parcours = models.CharField(
        max_length=100,
        verbose_name="Temps de parcours estimé",
        help_text="Ex: 2h30",
    )
    niveau_difficulte = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='facile',
        verbose_name="Niveau de difficulté",
    )
    distance_km = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name="Distance (km)",
        help_text="Ex: 12.5",
    )
    adresse_depart = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Lieu de départ",
        help_text="Adresse ou point de repère.",
    )
    image_principale = models.ImageField(
        upload_to="images/randonnees/",
        blank=True,
        null=True,
        verbose_name="Image de présentation",
        validators=[validate_image_upload],
    )
    carte_image = models.ImageField(
        upload_to="images/randonnees/cartes/",
        blank=True,
        null=True,
        verbose_name="Image de la carte du tracé",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "Randonnée"
        verbose_name_plural = "Randonnées"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class PeriscolaireInfo(BaseModel):
    titre = models.CharField(max_length=255, default="Inscription aux services périscolaires", verbose_name="Titre de la section")
    presentation = models.TextField(blank=True, verbose_name="Texte de présentation", help_text="Ce texte s'affichera au-dessus du formulaire d'inscription.")
    reglement_cantine_pdf = models.FileField(upload_to="documents/periscolaire/", blank=True, null=True, verbose_name="Règlement de la cantine (PDF)", validators=[validate_pdf_upload])
    reglement_garderie_pdf = models.FileField(upload_to="documents/periscolaire/", blank=True, null=True, verbose_name="Règlement de la garderie (PDF)", validators=[validate_pdf_upload])

    class Meta:
        verbose_name = "Information Périscolaire"
        verbose_name_plural = "Informations Périscolaires"

    def __str__(self):
        return self.titre