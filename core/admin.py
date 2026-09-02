"""
Configuration de l'interface d'administration Django (Back-office).

Ce fichier sert à définir comment les données (modèles) de la base de données 
seront affichées, gérées et modifiées dans l'interface sécurisée de l'administration (généralement /admin).
Il est utilisé chaque fois qu'un administrateur ou employé de la mairie se connecte 
pour ajouter, modifier ou supprimer du contenu (une actualité, un lieu, etc.) 
sans avoir besoin de toucher au code informatique ou à la base de données directement.
"""
from django.contrib import admin
from .models import (CommuneInfo, News, MunicipalCouncilReport, Association, School, SportFacilityType, SportFacility, HealthCenter, HealthcareProfessional, Pharmacy, SeniorResidence, Nursery, WasteCollectionSchedule, RecyclingCenter, RecyclingCenterSchedule, QuickLink, CommuneMedia, HistoireDhuizon, PatrimoineItem, Commerce, CommerceSchedule, Entreprise, EntrepriseSchedule, AuditLog, MenuCantine)

@admin.register(CommuneInfo)
class CommuneInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "population", "superficie_ha", "email", "telephone")
    readonly_fields = ("created_at", "updated_at")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "event_date", "author", "is_published")
    # list_filter ajoute un menu latéral pour filtrer les résultats (ex: voir seulement les articles publiés)
    list_filter = ("is_published", "event_date")
    search_fields = ("title", "content", "author")
    # prepopulated_fields remplit automatiquement le champ "slug" (URL) en fonction du titre
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "event_date"

@admin.register(MunicipalCouncilReport)
class MunicipalCouncilReportAdmin(admin.ModelAdmin):
    list_display = ("titre", "date")
    list_filter = ("date",)
    search_fields = ("titre", "description")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "date"

@admin.register(Association)
class AssociationAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone", "site_web")
    search_fields = ("nom", "description")
    readonly_fields = ("created_at", "updated_at")

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("nom", "nom_directrice", "nb_eleves", "telephone", "email")
    search_fields = ("nom", "nom_directrice")
    readonly_fields = ("created_at", "updated_at")

@admin.register(SportFacilityType)
class SportFacilityTypeAdmin(admin.ModelAdmin):
    list_display = ("nom", "icone")
    search_fields = ("nom",)
    readonly_fields = ("created_at", "updated_at")

class SportFacilityInline(admin.TabularInline):
    model = SportFacility
    extra = 0 # Nombre de formulaires vides affichés par défaut pour ajouter de nouveaux éléments
    fields = ("nom", "adresse", "description")

@admin.register(SportFacility)
class SportFacilityAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_equipement", "adresse")
    list_filter = ("type_equipement",)
    search_fields = ("nom", "adresse")
    readonly_fields = ("created_at", "updated_at")

class HealthcareProfessionalInline(admin.TabularInline):
    model = HealthcareProfessional
    extra = 0
    fields = ("prenom", "nom", "profession", "telephone", "email")

@admin.register(HealthCenter)
class HealthCenterAdmin(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "email")
    search_fields = ("nom", "adresse")
    readonly_fields = ("created_at", "updated_at")
    inlines = [HealthcareProfessionalInline]

@admin.register(HealthcareProfessional)
class HealthcareProfessionalAdmin(admin.ModelAdmin):
    list_display = ("__str__", "centre", "telephone", "email")
    list_filter = ("centre", "profession")
    search_fields = ("nom", "prenom", "profession")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "email")
    search_fields = ("nom",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(SeniorResidence)
class SeniorResidenceAdmin(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "email")
    search_fields = ("nom",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "email")
    search_fields = ("nom",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(WasteCollectionSchedule)
class WasteCollectionScheduleAdmin(admin.ModelAdmin):
    list_display = ("type_dechet", "jour", "heure", "description")
    list_filter = ("type_dechet", "jour")
    readonly_fields = ("created_at", "updated_at")

class RecyclingCenterScheduleInline(admin.TabularInline):
    model = RecyclingCenterSchedule
    extra = 0
    fields = ("saison", "jour", "heure_ouverture", "heure_fermeture", "ferme")

@admin.register(RecyclingCenter)
class RecyclingCenterAdmin(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "email")
    search_fields = ("nom",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [RecyclingCenterScheduleInline]

@admin.register(RecyclingCenterSchedule)
class RecyclingCenterScheduleAdmin(admin.ModelAdmin):
    list_display = ("centre", "saison", "jour", "heure_ouverture", "heure_fermeture", "ferme")
    list_filter = ("centre", "saison", "jour", "ferme")
    readonly_fields = ("created_at", "updated_at")

@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "icon_display", "url", "order")
    list_editable = ("order",)
    search_fields = ("label", "icon", "url")
    readonly_fields = ("created_at", "updated_at", "icon_display")
    
    def icon_display(self, obj):
        return obj.get_icon_display()
    icon_display.short_description = "Icône"

@admin.register(CommuneMedia)
class CommuneMediaAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_hero", "image")
    list_editable = ("order", "is_hero")
    search_fields = ("title", "description")
    readonly_fields = ("created_at", "updated_at")

@admin.register(HistoireDhuizon)
class HistoireDhuizonAdmin(admin.ModelAdmin):
    list_display = ("date_label", "evenement", "order")
    list_editable = ("order",)
    search_fields = ("date_label", "evenement")
    readonly_fields = ("created_at", "updated_at")

@admin.register(PatrimoineItem)
class PatrimoineItemAdmin(admin.ModelAdmin):
    list_display = ("nom", "description", "order")
    list_editable = ("order",)
    search_fields = ("nom", "description")
    readonly_fields = ("created_at", "updated_at")

class CommerceScheduleInline(admin.TabularInline):
    model = CommerceSchedule
    extra = 0
    max_num = 30
    can_delete = True
    fields = ("jour", "heure_ouverture", "heure_fermeture", "ferme")
    ordering = ["jour", "heure_ouverture"]
    verbose_name = "Créneau horaire"
    verbose_name_plural = "Créneaux horaires"

@admin.register(Commerce)
class CommerceAdmin(admin.ModelAdmin):
    list_display = ("nom_activite", "adresse", "personnel", "telephone", "order")
    list_editable = ("order",)
    search_fields = ("nom_activite", "adresse", "personnel")
    readonly_fields = ("created_at", "updated_at")
    inlines = [CommerceScheduleInline]

@admin.register(CommerceSchedule)
class CommerceScheduleAdmin(admin.ModelAdmin):
    list_display = ("commerce", "jour", "heure_ouverture", "heure_fermeture", "ferme")
    list_filter = ("commerce", "jour", "ferme")
    readonly_fields = ("created_at", "updated_at")

class EntrepriseScheduleInline(admin.TabularInline):
    model = EntrepriseSchedule
    extra = 0
    max_num = 30
    can_delete = True
    fields = ("jour", "heure_ouverture", "heure_fermeture", "ferme")
    ordering = ["jour", "heure_ouverture"]
    verbose_name = "Créneau horaire"
    verbose_name_plural = "Créneaux horaires"

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ("nom_activite", "adresse", "personnel", "telephone", "order")
    list_editable = ("order",)
    search_fields = ("nom_activite", "adresse", "personnel")
    readonly_fields = ("created_at", "updated_at")
    inlines = [EntrepriseScheduleInline]

@admin.register(EntrepriseSchedule)
class EntrepriseScheduleAdmin(admin.ModelAdmin):
    list_display = ("entreprise", "jour", "heure_ouverture", "heure_fermeture", "ferme")
    list_filter = ("entreprise", "jour", "ferme")
    readonly_fields = ("created_at", "updated_at")

from .models import (
    CommuneInfoSchedule, PharmacySchedule, SeniorResidenceSchedule,
    AdminAllowedIP, NextCouncilMeeting, MunicipalCouncilor, Transport,
    LeisureCenter, ChildcareProfessional, GlassCollectionPoint,
    TextileCollectionPoint, Mediatheque, MediathequeSchedule,
    LieuTouristique, CabaneCocou, Hebergement, Gite,
    AgencePostale, AgencePostaleSchedule, DemarcheAdministrative, Randonnee
)

# Liste de modèles simples qui n'ont pas besoin d'un affichage personnalisé complexe
missing_models = [
    CommuneInfoSchedule, PharmacySchedule, SeniorResidenceSchedule,
    AdminAllowedIP, NextCouncilMeeting, MunicipalCouncilor, Transport,
    LeisureCenter, ChildcareProfessional, GlassCollectionPoint,
    TextileCollectionPoint, Mediatheque, MediathequeSchedule,
    LieuTouristique, CabaneCocou, Hebergement, Gite,
    AgencePostale, AgencePostaleSchedule, DemarcheAdministrative, Randonnee
]

# Boucle pour enregistrer automatiquement tous les modèles "simples" ci-dessus
for model in missing_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# ──────────────────────────────────────────────────────────────────────────────
#  Menu Cantine – saisie rapide pour le secrétariat
# ──────────────────────────────────────────────────────────────────────────────

class MenuCantineInline(admin.TabularInline):
    """
    Permet de saisir toute la semaine d'un coup sur une seule page :
    une ligne par jour (Lundi → Vendredi).
    """
    model = MenuCantine
    extra = 5          # 5 lignes vides affichées (une par jour ouvré)
    max_num = 5
    fields = ("jour", "entree", "plat_principal", "accompagnement", "dessert", "laitage", "note")
    ordering = ["jour"]
    verbose_name = "Repas"
    verbose_name_plural = "Repas de la semaine"
    can_delete = True


class MenuCantineWeekProxy(MenuCantine):
    """Proxy utilisé pour grouper les menus par semaine dans l'admin."""
    class Meta:
        proxy = True
        verbose_name = "Semaine de menu cantine"
        verbose_name_plural = "🍽️  Menus de la cantine (par semaine)"


@admin.register(MenuCantine)
class MenuCantineAdmin(admin.ModelAdmin):
    """
    Vue liste : toutes les entrées, classées par semaine puis par jour.
    Pratique pour modifier un plat rapidement.
    """
    list_display = ("semaine_fr", "get_jour_display", "plat_principal", "entree", "dessert")
    list_filter = ("semaine", "jour")
    list_editable = ()          # on garde le list_display propre
    search_fields = ("plat_principal", "entree", "dessert", "accompagnement")
    ordering = ["-semaine", "jour"]
    date_hierarchy = "semaine"

    fieldsets = (
        ("Semaine & Jour", {
            "fields": ("semaine", "jour"),
            "description": "👉 Sélectionnez le <b>lundi</b> de la semaine concernée et le jour du repas.",
        }),
        ("Menu", {
            "fields": ("entree", "plat_principal", "accompagnement", "laitage", "dessert"),
        }),
        ("Informations complémentaires", {
            "classes": ("collapse",),
            "fields": ("note",),
        }),
    )

    def semaine_fr(self, obj):
        """Affiche la date en format lisible."""
        return obj.semaine.strftime("Semaine du %d/%m/%Y")
    semaine_fr.short_description = "Semaine"
    semaine_fr.admin_order_field = "semaine"

# ------------------------------------------------------------------------------
#  Menu Cantine
# ------------------------------------------------------------------------------

@admin.register(MenuCantine)
class MenuCantineAdmin(admin.ModelAdmin):
    list_display = ("annee", "numero_semaine", "get_jour_display", "plat_principal", "entree", "dessert")
    list_filter = ("annee", "numero_semaine", "jour")
    search_fields = ("plat_principal", "entree", "dessert", "accompagnement")
    ordering = ["-annee", "-numero_semaine", "jour"]

    fieldsets = (
        ("Semaine & Jour", {
            "fields": ("annee", "numero_semaine", "jour"),
            "description": "?? Saisissez l'<b>ann�e</b> et le <b>num�ro de la semaine</b> concern�e.",
        }),
        ("Menu", {
            "fields": ("entree", "plat_principal", "accompagnement", "laitage", "dessert"),
        }),
        ("Informations compl�mentaires", {
            "classes": ("collapse",),
            "fields": ("note",),
        }),
    )
