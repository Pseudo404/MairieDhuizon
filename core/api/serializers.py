"""
serializers.py — Sérialisation JSON de tous les modèles pour l'API mobile.
"""
from rest_framework import serializers
from core.models import (
    CommuneInfo, CommuneInfoSchedule,
    News,
    Association,
    HealthCenter, HealthcareProfessional,
    Pharmacy, PharmacySchedule,
    SeniorResidence,
    WasteCollectionSchedule, RecyclingCenter, RecyclingCenterSchedule,
    GlassCollectionPoint, TextileCollectionPoint,
    LeisureCenter,
    Commerce, CommerceSchedule,
    Transport,
    AgencePostale, AgencePostaleSchedule,
    Mediatheque, MediathequeSchedule,
    LieuTouristique, CabaneCocou, Hebergement, Gite,
    SportFacility, SportFacilityType,
    Randonnee,
    MenuCantine,
    Defibrillateur,
    Signalement, SignalementPhoto,
)


# ── Commune ──────────────────────────────────────────────────────────────────

class CommuneInfoScheduleSerializer(serializers.ModelSerializer):
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = CommuneInfoSchedule
        fields = ['jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class CommuneInfoSerializer(serializers.ModelSerializer):
    horaires_planning = CommuneInfoScheduleSerializer(many=True, read_only=True)
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = CommuneInfo
        fields = [
            'presentation', 'population', 'superficie_ha', 'region',
            'adresse', 'email', 'telephone', 'horaires',
            'logo_url', 'horaires_planning'
        ]

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None


# ── Actualités ───────────────────────────────────────────────────────────────

class NewsSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'short_description', 'content',
            'image_url', 'event_date', 'author', 'created_at'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ── Associations ─────────────────────────────────────────────────────────────

class AssociationSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Association
        fields = [
            'id', 'nom', 'slug', 'description',
            'email', 'telephone', 'site_web', 'logo_url'
        ]

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return None


# ── Santé ────────────────────────────────────────────────────────────────────

class HealthcareProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthcareProfessional
        fields = [
            'id', 'prenom', 'nom', 'profession',
            'telephone', 'email', 'adresse', 'infos_complementaires', 'order'
        ]


class HealthCenterSerializer(serializers.ModelSerializer):
    professionnels = HealthcareProfessionalSerializer(many=True, read_only=True)

    class Meta:
        model = HealthCenter
        fields = ['id', 'nom', 'adresse', 'telephone', 'email', 'professionnels']


class PharmacyScheduleSerializer(serializers.ModelSerializer):
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = PharmacySchedule
        fields = ['jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class PharmacySerializer(serializers.ModelSerializer):
    horaires_planning = PharmacyScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Pharmacy
        fields = ['id', 'nom', 'adresse', 'telephone', 'email', 'horaires', 'horaires_planning']


class SeniorResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeniorResidence
        fields = ['id', 'nom', 'adresse', 'telephone', 'email', 'horaires']


# ── Défibrillateurs ──────────────────────────────────────────────────────────

class DefibrillateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defibrillateur
        fields = [
            'id', 'nom', 'adresse',
            'latitude', 'longitude',
            'description', 'est_actif'
        ]


# ── Déchets ──────────────────────────────────────────────────────────────────

class WasteCollectionScheduleSerializer(serializers.ModelSerializer):
    type_dechet_display = serializers.CharField(source='get_type_dechet_display', read_only=True)
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = WasteCollectionSchedule
        fields = ['id', 'type_dechet', 'type_dechet_display', 'jour', 'jour_display', 'heure', 'description']


class RecyclingCenterScheduleSerializer(serializers.ModelSerializer):
    saison_display = serializers.CharField(source='get_saison_display', read_only=True)
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = RecyclingCenterSchedule
        fields = ['saison', 'saison_display', 'jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class RecyclingCenterSerializer(serializers.ModelSerializer):
    horaires = RecyclingCenterScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = RecyclingCenter
        fields = ['id', 'nom', 'adresse', 'telephone', 'email', 'horaires']


class GlassCollectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlassCollectionPoint
        fields = ['id', 'nom', 'adresse', 'description', 'order']


class TextileCollectionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextileCollectionPoint
        fields = ['id', 'nom', 'adresse', 'description', 'order']


# ── Loisirs ──────────────────────────────────────────────────────────────────

class LeisureCenterSerializer(serializers.ModelSerializer):
    menu_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = LeisureCenter
        fields = [
            'id', 'nom', 'adresse', 'telephone', 'email',
            'horaires', 'description', 'menu_pdf_url'
        ]

    def get_menu_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.menu_pdf and request:
            return request.build_absolute_uri(obj.menu_pdf.url)
        return None


class SportFacilityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportFacilityType
        fields = ['id', 'nom', 'icone']


class SportFacilitySerializer(serializers.ModelSerializer):
    type_equipement = SportFacilityTypeSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SportFacility
        fields = [
            'id', 'nom', 'type_equipement', 'description',
            'adresse', 'latitude', 'longitude', 'image_url'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class RandonneeSerializer(serializers.ModelSerializer):
    image_principale_url = serializers.SerializerMethodField()
    carte_image_url = serializers.SerializerMethodField()
    niveau_display = serializers.CharField(source='get_niveau_difficulte_display', read_only=True)

    class Meta:
        model = Randonnee
        fields = [
            'id', 'nom', 'slug', 'description_courte', 'description_detaillee',
            'temps_parcours', 'niveau_difficulte', 'niveau_display',
            'distance_km', 'adresse_depart',
            'image_principale_url', 'carte_image_url', 'order'
        ]

    def get_image_principale_url(self, obj):
        request = self.context.get('request')
        if obj.image_principale and request:
            return request.build_absolute_uri(obj.image_principale.url)
        return None

    def get_carte_image_url(self, obj):
        request = self.context.get('request')
        if obj.carte_image and request:
            return request.build_absolute_uri(obj.carte_image.url)
        return None


# ── Tourisme ─────────────────────────────────────────────────────────────────

class LieuTouristiqueSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = LieuTouristique
        fields = [
            'id', 'nom', 'description', 'temps_trajet',
            'distance_km', 'lien', 'image_url', 'order'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class HebergementSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_hebergement_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Hebergement
        fields = [
            'id', 'nom', 'type_hebergement', 'type_display',
            'description', 'adresse', 'telephone', 'email', 'site_web', 'image_url', 'order'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class GiteSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Gite
        fields = [
            'id', 'nom', 'description', 'adresse',
            'telephone', 'email', 'site_web',
            'capacite', 'tarif', 'image_url', 'order'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CabaneCocouSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CabaneCocou
        fields = [
            'id', 'nom', 'description', 'statut', 'statut_display',
            'capacite', 'tarif', 'lien', 'image_url', 'order'
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ── Infos pratiques ──────────────────────────────────────────────────────────

class CommerceScheduleSerializer(serializers.ModelSerializer):
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = CommerceSchedule
        fields = ['jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class CommerceSerializer(serializers.ModelSerializer):
    horaires = CommerceScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Commerce
        fields = ['id', 'nom_activite', 'adresse', 'personnel', 'telephone', 'order', 'horaires']


class TransportSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_transport_display', read_only=True)

    class Meta:
        model = Transport
        fields = ['id', 'type_transport', 'type_display', 'nom', 'description', 'horaires', 'lien', 'order']


class AgencePostaleScheduleSerializer(serializers.ModelSerializer):
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = AgencePostaleSchedule
        fields = ['jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class AgencePostaleSerializer(serializers.ModelSerializer):
    horaires_planning = AgencePostaleScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = AgencePostale
        fields = ['id', 'nom', 'adresse', 'telephone', 'horaires', 'horaires_planning']


class MediathequeScheduleSerializer(serializers.ModelSerializer):
    jour_display = serializers.CharField(source='get_jour_display', read_only=True)

    class Meta:
        model = MediathequeSchedule
        fields = ['jour', 'jour_display', 'heure_ouverture', 'heure_fermeture', 'ferme']


class MediathequeSerializer(serializers.ModelSerializer):
    horaires_planning = MediathequeScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Mediatheque
        fields = ['id', 'nom', 'adresse', 'telephone', 'email', 'horaires', 'infos', 'horaires_planning']


# ── Menus Cantine ────────────────────────────────────────────────────────────

class MenuCantineSerializer(serializers.ModelSerializer):
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = MenuCantine
        fields = ['id', 'annee', 'numero_semaine', 'pdf_url', 'created_at']

    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf and request:
            return request.build_absolute_uri(obj.pdf.url)
        return None


# ── Signalement ──────────────────────────────────────────────────────────────

class SignalementPhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SignalementPhoto
        fields = ['id', 'image_url', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class SignalementCreateSerializer(serializers.ModelSerializer):
    """Serializer utilisé pour la création d'un signalement depuis l'app mobile."""

    class Meta:
        model = Signalement
        fields = [
            'categorie', 'description',
            'latitude', 'longitude', 'adresse_approximative',
            'email_signalant'
        ]


class SignalementSerializer(serializers.ModelSerializer):
    photos = SignalementPhotoSerializer(many=True, read_only=True)
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    statut_display = serializers.CharField(source='get_statut_display', read_only=True)

    class Meta:
        model = Signalement
        fields = [
            'id', 'categorie', 'categorie_display',
            'description', 'latitude', 'longitude', 'adresse_approximative',
            'statut', 'statut_display', 'email_signalant',
            'photos', 'created_at'
        ]
