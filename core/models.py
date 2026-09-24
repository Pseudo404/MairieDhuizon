"""
models.py â Site de mairie Django
Architecture de base de donnÃ©es propre, scalable et adaptÃ©e Ã  l'ORM Django.

Conventions :
- BaseModel abstrait pour Ã©viter la duplication de created_at / updated_at
- Champs verbose_name sur chaque modÃ¨le et chaque champ
- Choices centralisÃ©s dans les modÃ¨les concernÃ©s
- Slugs auto-gÃ©nÃ©rables (Ã  cÃ¢bler dans save() ou avec django-autoslug)
- ImageField : pensez Ã  configurer MEDIA_ROOT / MEDIA_URL dans settings.py
- FileField (PDF) : idem
- PostgreSQL : tous les types sont nativement supportÃ©s par le backend psycopg2
"""

import uuid
from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator, RegexValidator
from django.urls import reverse
from core.validators import validate_image_upload, validate_pdf_upload, validate_safe_link_url, validate_document_upload, validate_inscription_document_size

class BaseModel(models.Model):
    """ ModÃ¨le de base """
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
        verbose_name="Texte de prÃ©sentation de la commune",
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
        verbose_name="RÃ©gion",
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
        verbose_name="TÃ©lÃ©phone de la mairie",
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
        help_text="Logo affichÃ© dans le header du site et sur les formulaires. Laissez vide pour utiliser le logo par dÃ©faut.",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "Information commune"
        verbose_name_plural = "Informations commune"

    def __str__(self):
        return "Informations de la commune"

    def clean(self):
        """EmpÃªche la crÃ©ation d'une seconde instance (pattern singleton)."""
        from django.core.exceptions import ValidationError
        if not self.pk and CommuneInfo.objects.exists():
            raise ValidationError(
                "Une seule entrÃ©e 'Informations commune' est autorisÃ©e."
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
        verbose_name="FermÃ© ce jour",
    )

    class Meta:
        verbose_name = "Horaire mairie"
        verbose_name_plural = "Horaires mairie"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} â Mairie"

class News(BaseModel):
    """ ActualitÃ© """
    title = models.CharField(
        max_length=255,
        verbose_name="Titre",
    )
    slug = models.SlugField(
        max_length=270,
        unique=True,
        verbose_name="Slug (URL)",
        help_text="GÃ©nÃ©rÃ© automatiquement depuis le titre.",
    )
    short_description = models.TextField(
        max_length=500,
        verbose_name="Description courte",
        help_text="RÃ©sumÃ© affichÃ© sur la liste des actualitÃ©s.",
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
        verbose_name="Date de l'Ã©vÃ©nement",
        help_text="Date Ã  laquelle l'Ã©vÃ©nement se dÃ©roule.",
    )
    author = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Auteur",
        help_text="Optionnel â nom de l'auteur de l'article.",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="PubliÃ©",
    )

    class Meta:
        verbose_name = "ActualitÃ©"
        verbose_name_plural = "ActualitÃ©s"
        ordering = ["event_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-gÃ©nÃ©ration du slug Ã  la crÃ©ation."""
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
        help_text="Optionnel â rÃ©sumÃ© du conseil.",
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
        help_text="GÃ©nÃ©rÃ© automatiquement depuis le nom.",
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
        verbose_name="TÃ©lÃ©phone",
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
        """Auto-gÃ©nÃ©ration du slug Ã  la crÃ©ation."""
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
    """ Ãcole """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'Ã©cole",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse postale",
    )
    telephone = models.CharField(
        max_length=20,
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="Nombre d'Ã©lÃ¨ves",
    )
    nb_inscrits_rentree = models.PositiveIntegerField(
        verbose_name="Inscrits Ã  la derniÃ¨re rentrÃ©e",
    )
    horaires_cours = models.TextField(
        verbose_name="Horaires des cours",
        help_text="Exemple : Lun/Mar/Jeu/Ven 8h30-11h30 / 13h30-16h30",
    )

    class Meta:
        verbose_name = "Ãcole"
        verbose_name_plural = "Ãcoles"
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
        verbose_name="Type d'Ã©quipement",
    )
    icone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="IcÃ´ne (classe CSS ou emoji)",
        help_text="Optionnel â ex: 'fas fa-futbol' ou 'â½'",
    )

    class Meta:
        verbose_name = "Type d'Ã©quipement sportif"
        verbose_name_plural = "Types d'Ã©quipements sportifs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class SportFacility(BaseModel):
    """ Installation sportive """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'Ã©quipement",
    )
    type_equipement = models.ForeignKey(
        SportFacilityType,
        on_delete=models.PROTECT,
        related_name="equipements",
        verbose_name="Type d'Ã©quipement",
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
        verbose_name = "Ãquipement sportif"
        verbose_name_plural = "Ãquipements sportifs"
        ordering = ["type_equipement", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.type_equipement})"

class HealthCenter(BaseModel):
    """ Maison de santÃ© """
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
        verbose_name="TÃ©lÃ©phone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )

    class Meta:
        verbose_name = "Maison de santÃ©"
        verbose_name_plural = "Maisons de santÃ©"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#sante-{}".format(self.pk)

class HealthcareProfessional(BaseModel):
    """ Professionnel de santÃ© """
    centre = models.ForeignKey(
        HealthCenter,
        on_delete=models.CASCADE,
        related_name="professionnels",
        verbose_name="Maison de santÃ©",
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="PrÃ©nom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    profession = models.CharField(
        max_length=150,
        verbose_name="Profession",
        help_text="Exemple : MÃ©decin gÃ©nÃ©raliste, KinÃ©sithÃ©rapeuteâ¦",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="TÃ©lÃ©phone",
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
        help_text="Utile pour les praticiens hors maison de santÃ© (ex: dentistes).",
    )
    infos_complementaires = models.TextField(
        blank=True,
        verbose_name="Informations complÃ©mentaires",
        help_text="Horaires personnalisÃ©s, secteur conventionnel, informations d'accÃ¨sâ¦",
    )

    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les professionnels sont triÃ©s par ordre croissant, puis par profession et nom.",
    )

    class Meta:
        verbose_name = "Professionnel de santÃ©"
        verbose_name_plural = "Professionnels de santÃ©"
        ordering = ["order", "profession", "nom", "prenom"]

    def __str__(self):
        return f"{self.prenom} {self.nom} â {self.profession}"

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
        verbose_name="TÃ©lÃ©phone",
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Informations complÃ©mentaires",
        help_text="Ex. : garde de nuit, fermetures exceptionnellesâ¦ Les horaires pour le statut Â« ouvert / fermÃ© Â» se gÃ¨rent ci-dessous.",
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
        verbose_name="FermÃ© ce jour",
    )

    class Meta:
        verbose_name = "Horaire pharmacie"
        verbose_name_plural = "Horaires pharmacie"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} â {self.pharmacie.nom}"

class SeniorResidence(BaseModel):
    """ RÃ©sidence pour personnes Ã¢gÃ©es """
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
        verbose_name="TÃ©lÃ©phone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Informations complÃ©mentaires",
        help_text="PrÃ©cisions d'accueil. Les horaires pour le statut Â« ouvert / fermÃ© Â» se gÃ¨rent ci-dessous.",
    )

    class Meta:
        verbose_name = "RÃ©sidence senior"
        verbose_name_plural = "RÃ©sidences seniors"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

class SeniorResidenceSchedule(BaseSchedule):
    """ Horaires de la rÃ©sidence sÃ©nior """

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
        verbose_name="RÃ©sidence",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="FermÃ© ce jour",
    )

    class Meta:
        verbose_name = "Horaire rÃ©sidence seniors"
        verbose_name_plural = "Horaires rÃ©sidence seniors"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} â {self.residence.nom}"

class Nursery(BaseModel):
    """ CrÃ¨che """
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
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="Lien vers le site de la crÃ¨che",
        help_text="Lien vers le site de la crÃ¨che ou de la gestionnaire.",
    )

    logo = models.ImageField(
        upload_to="images/creches/",
        blank=True,
        null=True,
        verbose_name="Logo de la crÃ¨che",
        validators=[validate_image_upload],
    )

    class Meta:
        verbose_name = "CrÃ¨che"
        verbose_name_plural = "CrÃ¨ches"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
    
    def get_absolute_url(self):
        return "/vie-pratique#petite-enfance"

class WasteCollectionSchedule(BaseSchedule):
    """ Calendrier de collecte des dÃ©chets """

    class WasteType(models.TextChoices):
        MENAGERS       = "menagers",    "DÃ©chets mÃ©nagers"
        RECYCLABLES    = "recyclables", "Recyclables (tri sÃ©lectif)"
        VERRE          = "verre",       "Verre"
        ENCOMBRANTS    = "encombrants", "Encombrants"
        VEGETAUX       = "vegetaux",    "DÃ©chets verts / vÃ©gÃ©taux"
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
        verbose_name="Type de dÃ©chet",
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
        verbose_name="Description / prÃ©cisions",
    )

    class Meta:
        verbose_name = "Planning de collecte des dÃ©chets"
        verbose_name_plural = "Plannings de collecte des dÃ©chets"
        ordering = ["jour_index", "type_dechet"]
        unique_together = [("type_dechet", "jour")]

    def __str__(self):
        return f"{self.get_type_dechet_display()} â {self.get_jour_display()}"
    
    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"

class RecyclingCenter(BaseModel):
    """ DÃ©chetterie """
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
        verbose_name="TÃ©lÃ©phone",
    )
    email = models.EmailField(
        blank=True,
        validators=[EmailValidator()],
        verbose_name="Email",
    )

    class Meta:
        verbose_name = "DÃ©chetterie"
        verbose_name_plural = "DÃ©chetteries"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return "/vie-pratique#collecte-dechets"
    

class RecyclingCenterSchedule(BaseSchedule):
    """ Horaires de la dÃ©chetterie """

    class Season(models.TextChoices):
        ETE   = "ete",   "ÃtÃ© (01/04 â 31/10)"
        HIVER = "hiver", "Hiver (01/11 â 31/03)"

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
        verbose_name="DÃ©chetterie",
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
        verbose_name="FermÃ© ce jour",
        help_text="Cocher si la dÃ©chetterie est fermÃ©e ce jour-lÃ  pour cette saison.",
    )

    class Meta:
        verbose_name = "Horaire de dÃ©chetterie"
        verbose_name_plural = "Horaires de dÃ©chetterie"
        ordering = ["centre", "saison", "jour_index"]
        unique_together = [("centre", "saison", "jour")]

    def __str__(self):
        return (
            f"{self.centre} â {self.get_saison_display()} â "
            f"{self.get_jour_display()} : "
            f"{self.heure_ouverture:%H:%M}â{self.heure_fermeture:%H:%M}"
        )

class QuickLink(BaseModel):
    """ Lien rapide """
    ICONS_CHOICES = [
        ('school', 'ð'),
        ('sports_soccer', 'â½'),
        ('local_pharmacy', 'ð'),
        ('home', 'ð '),
        ('info', 'â¹ï¸'),
        ('restaurant', 'ð½ï¸'),
        ('room_service', 'ðï¸'),
        ('kebab_dining', 'ð¢'),
        ('local_pizza', 'ð'),
        ('partly_cloudy_day', 'â'),
        ('sunny', 'âï¸'),
        ('cloud', 'âï¸'),
        ('rainy_snow', 'ð§ï¸'),
        ('thunderstorm', 'âï¸'),
        ('rainy', 'ð§ï¸'),
        ('health_and_safety', 'ð©º'),
        ('health_cross', 'â'),
        ('location_on', 'ð'),
        ('phone', 'âï¸'),
        ('email', 'âï¸'),
        ('people', 'ð¥'),
        ('event', 'ð'),
        ('library_books', 'ð'),
        ('elderly_woman', 'ðµ'),
        ('child_care', 'ð¶'),
        ('recycling', 'â»ï¸'),
        ('delete', 'ðï¸'),
        ('medical_services', 'ð¥'),
        ('directions_car', 'ð'),
        ('shopping_cart', 'ð'),
        ('park', 'ð³'),
        ('directions', 'ðºï¸'),
        ('account_balance', 'ðï¸'),
        ('newspaper', 'ð°'),
        ('calendar_month', 'ð'),
        ('mail', 'ð§'),
        ('alarm', 'ð'),
        ('pin_drop', 'ð'),
        ('book_ribbon', 'ð'),
        ('celebration', 'ð'),
        ('construction', 'ðï¸'),
        ('home_repair_service', 'ð¨'),
        ('forest', 'ð²'),
        ('compost', 'â»ï¸'),
        ('how_to_vote', 'ð³ï¸'),
        ('diversity_3', 'ð¥'),
        ('trophy', 'ð'),
        ('comedy_mask', 'ð­'),
        ('festival', 'ðª'),
        ('shield', 'ð¡ï¸'),
        ('badge', 'ð®'),
        ('local_fire_department', 'ð¥'),
        ('map', 'ðºï¸'),
        ('church', 'âª'),
        ('file_export', 'ð'),
        ('assignment', 'ð'),
        ('photo', 'ð¼ï¸'),
        ('send', 'ð¨'),
        ('accessibility', 'â¿'),
    ]
    label = models.CharField(
        max_length=100,
        verbose_name="LibellÃ©",
        help_text="Texte affichÃ© sous l'icÃ´ne (ex: Ãcole, Sportâ¦)",
    )
    icon = models.CharField(
        max_length=50,
        choices=ICONS_CHOICES,
        verbose_name="IcÃ´ne",
        help_text="SÃ©lectionnez une icÃ´ne prÃ©dÃ©finie",
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
    """ MÃ©dia de la commune """
    title = models.CharField(
        max_length=200,
        verbose_name="Titre / lÃ©gende",
    )
    image = models.ImageField(
        upload_to="images/galerie/",
        verbose_name="Photo",
        validators=[validate_image_upload],
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Optionnel â description dÃ©taillÃ©e de la photo.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )
    is_hero = models.BooleanField(
        default=False,
        verbose_name="Image hÃ©ro (fond accueil)",
        help_text="Cocher pour utiliser cette photo comme fond de la section principale.",
    )
    is_hero_tourisme = models.BooleanField(
        default=False,
        verbose_name="Image hÃ©ro (fond tourisme)",
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
        verbose_name="Date / pÃ©riode",
        help_text="Texte affichÃ© comme repÃ¨re temporel (ex: 1000, XIXe siÃ¨cle, Aujourd'huiâ¦)",
    )
    evenement = models.TextField(
        verbose_name="ÃvÃ©nement",
        help_text="Description de l'Ã©vÃ©nement historique.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Les Ã©vÃ©nements sont affichÃ©s par ordre croissant.",
    )

    class Meta:
        verbose_name = "ÃvÃ©nement historique"
        verbose_name_plural = "ÃvÃ©nements historiques"
        ordering = ["order", "date_label"]

    def __str__(self):
        return f"{self.date_label} â {self.evenement[:50]}"

class PatrimoineItem(BaseModel):
    """ Patrimoine de Dhuizon """
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du lieu",
        help_text="Ex: Mairie, Ãglise Saint-Pierre, Ãtangsâ¦",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Texte affichÃ© sous le nom du lieu.",
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
        help_text="Les Ã©lÃ©ments sont affichÃ©s par ordre croissant.",
    )

    class Meta:
        verbose_name = "ÃlÃ©ment de patrimoine"
        verbose_name_plural = "ÃlÃ©ments de patrimoine"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

class AdminAllowedIP(BaseModel):
    """ IP autorisÃ©e pour l'administration """
    label = models.CharField(
        max_length=120,
        verbose_name="LibellÃ©",
        help_text="Ex. : Mairie de Dhuizon, Bureau du maireâ¦",
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
        verbose_name = "IP autorisÃ©e (/admin/)"
        verbose_name_plural = "IP autorisÃ©es (/admin/)"
        ordering = ['label', 'ip_address']

    def __str__(self):
        status = 'active' if self.is_active else 'inactive'
        return f'{self.label} â {self.ip_address} ({status})'

class AdminAccount(BaseModel):
    """ Compte Administrateur """
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='admin_account')
    is_super_admin = models.BooleanField(
        default=False,
        verbose_name="Est Super Admin (Mairie)",
        help_text="Les Super Admins peuvent crÃ©er et gÃ©rer d'autres administrateurs."
    )
    is_centre_loisirs = models.BooleanField(
        default=False,
        verbose_name="Est Admin Centre de Loisirs uniquement",
        help_text="AccÃ¨s restreint au panneau de gestion du centre de loisirs (pas d'accÃ¨s au panel gÃ©nÃ©ral)."
    )
    can_access_centre_loisirs = models.BooleanField(
        default=False,
        verbose_name="AccÃ¨s Centre de Loisirs",
        help_text="En plus de l'accÃ¨s au panel gÃ©nÃ©ral, cet admin peut aussi accÃ©der au centre de loisirs."
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
        verbose_name="Page visitÃ©e",
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
        verbose_name="ClÃ© de session",
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
        return f"{self.path} â {self.created_at:%d/%m/%Y %H:%M}"

class NextCouncilMeeting(BaseModel):
    """ Prochaine rÃ©union du conseil """
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
            raise ValidationError("Une seule entrÃ©e est autorisÃ©e.")
        
    def get_absolute_url(self):
        return "/conseil-municipal#prochain-conseil"

class MunicipalCouncilor(BaseModel):
    """ Conseiller municipaux """
    prenom = models.CharField(
        max_length=100,
        verbose_name="PrÃ©nom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    role = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="RÃ´le / fonction",
        help_text="Ex: Maire, Adjoint au maire, Conseiller municipalâ¦",
    )
    comissions = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Commissions",
        help_text="Ex: Urbanisme, Environnement, Cultureâ¦",
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
        return f"{self.prenom} {self.nom} â {self.role}"
    
    def get_absolute_url(self):
        return "/conseil-municipal#elus"

class Transport(BaseModel):
    """ Transport """

    class TransportType(models.TextChoices):
        SCOLAIRE  = "scolaire",  "Transport scolaire"
        REGULIER  = "regulier",  "Transport rÃ©gulier"

    type_transport = models.CharField(
        max_length=20,
        choices=TransportType.choices,
        verbose_name="Type",
    )
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom / numÃ©ro de ligne",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
        help_text="Trajet, arrÃªts, frÃ©quenceâ¦",
    )
    horaires = models.TextField(
        blank=True,
        verbose_name="Horaires",
    )
    lien = models.URLField(
        blank=True,
        verbose_name="Lien",
        help_text="Lien vers le site de l'opÃ©rateur ou les horaires en ligne.",
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
        return f"{self.get_type_transport_display()} â {self.nom}"
    
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
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="CapacitÃ© journaliÃ¨re maximale",
        help_text="Nombre maximum d'enfants pouvant Ãªtre accueillis par jour."
    )
    menu_pdf = models.FileField(
        upload_to="documents/centre_loisirs/",
        blank=True,
        null=True,
        verbose_name="Menu (PDF)",
        validators=[validate_pdf_upload],
        help_text="Un seul PDF contenant le menu pour le centre de loisirs."
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
        choices=[('ouvert', 'Ouvert'), ('ferme', 'FermÃ©'), ('ferie', 'FÃ©riÃ©')],
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
    prenom_enfant = models.CharField(max_length=100, verbose_name="PrÃ©nom de l'enfant")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    
    nom_responsable_1 = models.CharField(max_length=100, verbose_name="Nom (Responsable 1)")
    prenom_responsable_1 = models.CharField(max_length=100, verbose_name="PrÃ©nom (Responsable 1)")
    adresse_responsable_1 = models.CharField(max_length=255, verbose_name="Adresse (Responsable 1)")
    code_postal_1 = models.CharField(max_length=20, verbose_name="Code postal (Responsable 1)")
    ville_1 = models.CharField(max_length=100, verbose_name="Ville (Responsable 1)")
    telephone_1 = models.CharField(max_length=20, blank=True, verbose_name="TÃ©lÃ©phone (Responsable 1)")
    portable_1 = models.CharField(max_length=20, verbose_name="Portable (Responsable 1)")
    email_1 = models.EmailField(verbose_name="Email (Responsable 1)")

    nom_responsable_2 = models.CharField(max_length=100, blank=True, verbose_name="Nom (Responsable 2)")
    prenom_responsable_2 = models.CharField(max_length=100, blank=True, verbose_name="PrÃ©nom (Responsable 2)")
    adresse_responsable_2 = models.CharField(max_length=255, blank=True, verbose_name="Adresse (Responsable 2)")
    code_postal_2 = models.CharField(max_length=20, blank=True, verbose_name="Code postal (Responsable 2)")
    ville_2 = models.CharField(max_length=100, blank=True, verbose_name="Ville (Responsable 2)")
    telephone_2 = models.CharField(max_length=20, blank=True, verbose_name="TÃ©lÃ©phone (Responsable 2)")
    portable_2 = models.CharField(max_length=20, blank=True, verbose_name="Portable (Responsable 2)")
    email_2 = models.EmailField(blank=True, verbose_name="Email (Responsable 2)")

    coefficient_familial = models.CharField(max_length=50, blank=True, verbose_name="Coefficient familial")
    justificatif_quotient_familial = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="Justificatif quotient familial")
    
    livret_famille = models.BooleanField(default=False, verbose_name="Livret de famille fourni (Ancien)")
    livret_famille_doc = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="Livret de famille (Document)")
    jugement_familial = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="Jugement familial")
    personnes_habilitees_identite = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="PiÃ¨ce d'identitÃ© (Personnes habilitÃ©es)")
    personnes_habilitees_texte = models.TextField(blank=True, verbose_name="Personnes habilitÃ©es Ã  venir chercher l'enfant")
    
    pai_sante = models.TextField(blank=True, verbose_name="PAI informations de santÃ© (lunettes, fauteuil, etc.)")
    vaccins = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="Vaccins")
    assurance_scolaire = models.FileField(upload_to='inscriptions_cl/', validators=[validate_document_upload, validate_inscription_document_size], blank=True, null=True, verbose_name="Assurance extra-scolaire")

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Lien vers une inscription prÃ©cÃ©dente dont les documents sont rÃ©utilisÃ©s
    docs_source = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='inscriptions_utilisant_ces_docs',
        verbose_name="Documents repris depuis l'inscription",
        help_text="Si la famille n'a pas fourni de nouveaux fichiers, pointe vers l'inscription prÃ©cÃ©dente qui possÃ¨de les documents.",
    )

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

    def get_doc_effectif(self, field_name):
        """
        Retourne le fichier effectif pour un champ document donnÃ©.
        Si le champ est vide sur cette inscription, on remonte vers docs_source
        (une seule gÃ©nÃ©ration), puis on retourne None si toujours vide.
        """
        value = getattr(self, field_name)
        if value and value.name:
            return value
        if self.docs_source_id:
            source_value = getattr(self.docs_source, field_name)
            if source_value and source_value.name:
                return source_value
        return None

    @property
    def docs_effectifs(self):
        """
        Retourne un dict {field_name: FileField ou None} en rÃ©solvant chaque
        document champ par champ : on prend le fichier de cette inscription
        s'il existe, sinon celui de docs_source.
        """
        doc_fields = [
            'justificatif_quotient_familial',
            'livret_famille_doc',
            'jugement_familial',
            'personnes_habilitees_identite',
            'vaccins',
            'assurance_scolaire',
        ]
        return {f: self.get_doc_effectif(f) for f in doc_fields}

    @property
    def docs_source_date(self):
        """Date de crÃ©ation de l'inscription source des documents (si applicable)."""
        if self.docs_source_id:
            return self.docs_source.created_at
        return None

class ReservationCentreLoisirs(BaseModel):
    """ Une rÃ©servation pour un jour donnÃ© """
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'ValidÃ©e'),
        ('refusee', 'RefusÃ©e'),
        ('annulee', 'AnnulÃ©e'),
    ]
    inscription = models.ForeignKey('InscriptionCentreLoisirs', on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField(verbose_name="Date rÃ©servÃ©e")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    token_annulation = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation/refus")
    validee_par = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations_validees')
    motif_refus = models.CharField(max_length=255, blank=True, verbose_name="Motif de refus")

    class Meta:
        verbose_name = "RÃ©servation centre de loisirs"
        verbose_name_plural = "RÃ©servations centre de loisirs"
        unique_together = ('inscription', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.inscription} - {self.date.strftime('%d/%m/%Y')} ({self.get_statut_display()})"

class ChildcareProfessional(BaseModel):
    """ Nourisses """
    prenom = models.CharField(
        max_length=100,
        verbose_name="PrÃ©nom",
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="Nom / libellÃ©",
        help_text="Ex: Parking de la Mairie, Rue de la ForÃªtâ¦",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description / prÃ©cisions",
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
        verbose_name="Nom / libellÃ©",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description / prÃ©cisions",
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
    """ MÃ©diathÃ¨que """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom",
        default="MÃ©diathÃ¨que de Dhuizon",
    )
    adresse = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="Informations complÃ©mentaires",
    )

    class Meta:
        verbose_name = "MÃ©diathÃ¨que"
        verbose_name_plural = "MÃ©diathÃ¨que"

    def __str__(self):
        return self.nom

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.pk and Mediatheque.objects.exists():
            raise ValidationError("Une seule entrÃ©e mÃ©diathÃ¨que est autorisÃ©e.")
        
    def get_absolute_url(self):
        return "/vie-pratique#mairie-mediatheque"

class MediathequeSchedule(BaseSchedule):
    """ Horaires de la mÃ©diathÃ¨que """
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
        verbose_name="MÃ©diathÃ¨que",
    )
    jour = models.CharField(max_length=10, choices=Weekday.choices, verbose_name="Jour")
    heure_ouverture = models.TimeField(verbose_name="Heure d'ouverture")
    heure_fermeture = models.TimeField(verbose_name="Heure de fermeture")
    ferme = models.BooleanField(
        default=False,
        verbose_name="FermÃ© ce jour",
    )

    class Meta:
        verbose_name = "Horaire mÃ©diathÃ¨que"
        verbose_name_plural = "Horaires mÃ©diathÃ¨que"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} â {self.mediatheque.nom}"

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
        help_text="Ex : 15 min en voiture, 30 min Ã  vÃ©loâ¦",
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
        EN_PROJET      = "en_projet",      "ð En projet"
        EN_CONSTRUCTION = "en_construction", "ð§ En construction"
        OUVERT         = "ouvert",         "â Ouvert"

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
        verbose_name="CapacitÃ© (personnes)",
    )
    tarif = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Tarif indicatif",
        help_text="Ex : Ã partir de 120â¬/nuit",
    )
    lien = models.URLField(
        blank=True,
        validators=[validate_safe_link_url],
        verbose_name="Lien de rÃ©servation / site",
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
    """ HÃ©bergement """
    class TypeHebergement(models.TextChoices):
        AUBERGE = "auberge", "Auberge"
        HOTEL   = "hotel",   "HÃ´tel"
        GITE    = "gite",    "GÃ®te"
        CAMPING = "camping", "Camping"
        AUTRE   = "autre",   "Autre"

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de l'hÃ©bergement",
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
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name = "HÃ©bergement"
        verbose_name_plural = "HÃ©bergements"
        ordering = ["order", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.get_type_hebergement_display()})"
    
    def get_absolute_url(self):
        return "/tourisme#hebergements"

class Gite(BaseModel):
    """ GÃ®te """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom du gÃ®te",
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
        verbose_name="TÃ©lÃ©phone",
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
        verbose_name="CapacitÃ© (personnes)",
    )
    tarif = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tarif indicatif",
        help_text="Ex : Ã partir de 80 â¬ / nuit",
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
        verbose_name = "GÃ®te"
        verbose_name_plural = "GÃ®tes"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return "/tourisme#gites"

class Commerce(BaseModel):
    """ Commerce """
    nom_activite = models.CharField(
        max_length=255,
        verbose_name="Nom de l'activitÃ©",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    personnel = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Personnel / Responsable",
        help_text="Nom(s) du ou des responsables / gÃ©rants.",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="TÃ©lÃ©phone",
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
        help_text="Laisser vide si fermÃ© toute la journÃ©e.",
    )
    heure_fermeture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure de fermeture",
        help_text="Laisser vide si fermÃ© toute la journÃ©e.",
    )
    ferme = models.BooleanField(
        default=False,
        verbose_name="FermÃ© ce jour",
        help_text="Cocher si le commerce est fermÃ© ce jour-lÃ .",
    )

    class Meta:
        verbose_name = "Horaire commerce"
        verbose_name_plural = "Horaires commerce"
        ordering = ["commerce", "jour_index", "heure_ouverture"]

    def __str__(self):
        if self.ferme:
            return f"{self.get_jour_display()} â {self.commerce.nom_activite} : FermÃ©"
        if self.heure_ouverture and self.heure_fermeture:
            return (
                f"{self.get_jour_display()} â {self.commerce.nom_activite} : "
                f"{self.heure_ouverture:%H:%M}â{self.heure_fermeture:%H:%M}"
            )
        return f"{self.get_jour_display()} â {self.commerce.nom_activite} : Non renseignÃ©"

class Entreprise(BaseModel):
    """ Entreprises """
    nom_activite = models.CharField(
        max_length=255,
        verbose_name="Nom de l'activitÃ©",
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse",
    )
    personnel = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Personnel / Responsable",
        help_text="Nom(s) du ou des responsables / gÃ©rants.",
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="TÃ©lÃ©phone",
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
        help_text="Laisser vide si fermÃ© toute la journÃ©e.",
    )
    heure_fermeture = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Heure de fermeture",
        help_text="Laisser vide si fermÃ© toute la journÃ©e.",
    )
    ferme = models.BooleanField(
        default=False,
        verbose_name="FermÃ© ce jour",
        help_text="Cocher si l'entreprise est fermÃ©e ce jour-lÃ .",
    )

    class Meta:
        verbose_name = "Horaire entreprise"
        verbose_name_plural = "Horaires entreprise"
        ordering = ["entreprise", "jour_index", "heure_ouverture"]

    def __str__(self):
        if self.ferme:
            return f"{self.get_jour_display()} â {self.entreprise.nom_activite} : FermÃ©"
        if self.heure_ouverture and self.heure_fermeture:
            return (
                f"{self.get_jour_display()} â {self.entreprise.nom_activite} : "
                f"{self.heure_ouverture:%H:%M}â{self.heure_fermeture:%H:%M}"
            )
        return f"{self.get_jour_display()} â {self.entreprise.nom_activite} : Non renseignÃ©"

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
        verbose_name="TÃ©lÃ©phone",
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
            raise ValidationError("Une seule entrÃ©e agence postale est autorisÃ©e.")
        
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
        verbose_name="FermÃ© ce jour",
    )

    class Meta:
        verbose_name = "Horaire agence postale"
        verbose_name_plural = "Horaires agence postale"
        ordering = ["jour_index", "heure_ouverture"]

    def __str__(self):
        return f"{self.get_jour_display()} â {self.agence_postale.nom}"

class DemarcheAdministrative(BaseModel):
    """ DÃ©marche administrative """
    titre = models.CharField(max_length=255, verbose_name="Titre de la dÃ©marche")
    description = models.TextField(verbose_name="Description / Explications", blank=True)
    lien_service_public = models.URLField(verbose_name="Lien externe (ex: service-public.fr)", blank=True)
    fichier_pdf = models.FileField(upload_to="demarches/", validators=[validate_pdf_upload], verbose_name="Fichier PDF Ã  tÃ©lÃ©charger (ex: CERFA)", blank=True, null=True)
    icone = models.CharField(max_length=50, default="article", verbose_name="IcÃ´ne Google Material", help_text="Ex: 'description', 'favorite', 'home'")
    ordre = models.PositiveSmallIntegerField(default=10, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "DÃ©marche administrative"
        verbose_name_plural = "DÃ©marches administratives"
        ordering = ["ordre", "titre"]

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return "/vie-pratique/#demarches"

class AuditLog(models.Model):
    """ Journal d'audit """
    class Action(models.TextChoices):
        CREE     = "cree",      "CrÃ©Ã©"
        MODIFIE  = "modifie",   "ModifiÃ©"
        SUPPRIME = "supprime",  "SupprimÃ©"

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
        help_text="Slug de la section concernÃ©e (ex : sante-professionnels)",
    )
    section_label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="LibellÃ© de la section",
    )
    model_name = models.CharField(
        max_length=100,
        verbose_name="ModÃ¨le concernÃ©",
        help_text="Nom du modÃ¨le Django (ex : HealthcareProfessional)",
    )
    object_pk = models.CharField(
        max_length=50,
        verbose_name="ID de l'objet",
    )
    object_repr = models.CharField(
        max_length=500,
        verbose_name="ReprÃ©sentation de l'objet",
        help_text="Valeur __str__ de l'objet au moment de l'action",
    )
    changes = models.TextField(
        blank=True,
        verbose_name="DÃ©tail des modifications",
        help_text="JSON : champs modifiÃ©s avec valeurs avant / aprÃ¨s",
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
        user_str = self.user.get_full_name() or self.user.username if self.user else "SystÃ¨me"
        return f"[{self.get_action_display()}] {self.object_repr} par {user_str} â {self.created_at:%d/%m/%Y %H:%M}"

    def get_changes_display(self):
        """DÃ©sÃ©rialise le JSON des modifications pour affichage."""
        import json
        if not self.changes:
            return []
        try:
            return json.loads(self.changes)
        except (json.JSONDecodeError, ValueError):
            return []

class Randonnee(BaseModel):
    """ RandonnÃ©e """
    NIVEAU_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]

    nom = models.CharField(
        max_length=255,
        verbose_name="Nom de la randonnÃ©e",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name="Slug (URL)",
        help_text="GÃ©nÃ©rÃ© automatiquement si laissÃ© vide.",
    )
    description_courte = models.CharField(
        max_length=500,
        verbose_name="Description courte",
        help_text="AffichÃ©e sur la carte dans la liste des loisirs.",
    )
    description_detaillee = models.TextField(
        verbose_name="Description dÃ©taillÃ©e",
        help_text="AffichÃ©e sur la page dÃ©diÃ©e Ã  la randonnÃ©e.",
    )
    temps_parcours = models.CharField(
        max_length=100,
        verbose_name="Temps de parcours estimÃ©",
        help_text="Ex: 2h30",
    )
    niveau_difficulte = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='facile',
        verbose_name="Niveau de difficultÃ©",
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
        verbose_name="Lieu de dÃ©part",
        help_text="Adresse ou point de repÃ¨re.",
    )
    image_principale = models.ImageField(
        upload_to="images/randonnees/",
        blank=True,
        null=True,
        verbose_name="Image de prÃ©sentation",
        validators=[validate_image_upload],
    )
    carte_image = models.ImageField(
        upload_to="images/randonnees/cartes/",
        blank=True,
        null=True,
        verbose_name="Image de la carte du tracÃ©",
        validators=[validate_image_upload],
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
    )

    class Meta:
        verbose_name = "RandonnÃ©e"
        verbose_name_plural = "RandonnÃ©es"
        ordering = ["order", "nom"]

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

class PeriscolaireInfo(BaseModel):
    titre = models.CharField(max_length=255, default="Inscription aux services pÃ©riscolaires", verbose_name="Titre de la section")
    presentation = models.TextField(blank=True, verbose_name="Texte de prÃ©sentation", help_text="Ce texte s'affichera au-dessus du formulaire d'inscription.")
    reglement_cantine_pdf = models.FileField(upload_to="documents/periscolaire/", blank=True, null=True, verbose_name="RÃ¨glement de la cantine (PDF)", validators=[validate_pdf_upload])
    reglement_garderie_pdf = models.FileField(upload_to="documents/periscolaire/", blank=True, null=True, verbose_name="RÃ¨glement de la garderie (PDF)", validators=[validate_pdf_upload])

    class Meta:
        verbose_name = "Information PÃ©riscolaire"
        verbose_name_plural = "Informations PÃ©riscolaires"

    def __str__(self):
        return self.titre


import datetime

def current_year():
    return datetime.date.today().isocalendar()[0]

def current_week():
    return datetime.date.today().isocalendar()[1]

class MenuCantine(BaseModel):
    """
    Menu hebdomadaire de la cantine scolaire en PDF.
    Le secrÃ©tariat uploade un PDF par semaine.
    """
    annee = models.IntegerField(
        verbose_name="AnnÃ©e",
        default=current_year,
        help_text="Exemple : 2024",
    )
    numero_semaine = models.IntegerField(
        verbose_name="NumÃ©ro de la semaine",
        default=current_week,
        help_text="Exemple : 34",
    )
    pdf = models.FileField(
        upload_to="documents/cantine/",
        blank=True,
        null=True,
        verbose_name="Fichier PDF du menu",
        validators=[validate_pdf_upload],
        help_text="Un seul PDF par semaine."
    )

    class Meta:
        verbose_name = "Menu de la cantine"
        verbose_name_plural = "Menus de la cantine"
        ordering = ["-annee", "-numero_semaine"]
        unique_together = [("annee", "numero_semaine")]

    def __str__(self):
        return f"Menu cantine â Semaine {self.numero_semaine} ({self.annee})"



class Defibrillateur(BaseModel):
    """ Défibrillateur automatisé externe (DAE) """
    nom = models.CharField(
        max_length=255,
        verbose_name="Nom / lieu",
        help_text="Ex: Mairie, Salle des fêtes, École..."
    )
    adresse = models.CharField(
        max_length=255,
        verbose_name="Adresse"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitude GPS"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitude GPS"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Informations complémentaires",
        help_text="Accès, disponibilité 24h/24, étage..."
    )
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Décocher si le défibrillateur est hors service."
    )

    class Meta:
        verbose_name = "Défibrillateur (DAE)"
        verbose_name_plural = "Défibrillateurs (DAE)"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} — {self.adresse}"


class Signalement(BaseModel):
    """ Signalement d'un habitant à la mairie """

    class Categorie(models.TextChoices):
        VOIRIE         = 'voirie',        'Voirie / Route'
        ECLAIRAGE      = 'eclairage',     'Éclairage public'
        DECHETS        = 'dechets',       'Déchets / Propreté'
        ESPACES_VERTS  = 'espaces_verts', 'Espaces verts'
        BATIMENT       = 'batiment',      'Bâtiment communal'
        AUTRE          = 'autre',         'Autre'

    class Statut(models.TextChoices):
        NOUVEAU   = 'nouveau',   '🆕 Nouveau'
        EN_COURS  = 'en_cours',  '🔄 En cours de traitement'
        RESOLU    = 'resolu',    '✅ Résolu'
        REJETE    = 'rejete',    '❌ Rejeté'

    categorie = models.CharField(
        max_length=20,
        choices=Categorie.choices,
        verbose_name="Catégorie"
    )
    description = models.TextField(
        verbose_name="Description du problème"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Latitude GPS"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Longitude GPS"
    )
    adresse_approximative = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Adresse approximative",
        help_text="Fournie par l'habitant ou calculée depuis les coordonnées GPS."
    )
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.NOUVEAU,
        verbose_name="Statut"
    )
    email_signalant = models.EmailField(
        blank=True,
        verbose_name="Email du signalant (optionnel)",
        help_text="Pour pouvoir notifier l'habitant du traitement de son signalement."
    )
    commentaire_mairie = models.TextField(
        blank=True,
        verbose_name="Commentaire interne mairie"
    )

    class Meta:
        verbose_name = "Signalement"
        verbose_name_plural = "Signalements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_categorie_display()}] {self.description[:60]} — {self.get_statut_display()}"


class SignalementPhoto(BaseModel):
    """ Photo attachée à un signalement """
    signalement = models.ForeignKey(
        Signalement,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name="Signalement"
    )
    image = models.ImageField(
        upload_to='signalements/',
        verbose_name="Photo"
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Ordre"
    )

    class Meta:
        verbose_name = "Photo de signalement"
        verbose_name_plural = "Photos de signalement"
        ordering = ["order"]

    def __str__(self):
        return f"Photo #{self.order} — {self.signalement}"
