"""
views.py — Vues API REST pour l'app mobile Mairie de Dhuizon.
"""
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail

from core.models import (
    CommuneInfo,
    News,
    Association,
    HealthCenter,
    Pharmacy,
    SeniorResidence,
    WasteCollectionSchedule, RecyclingCenter,
    GlassCollectionPoint, TextileCollectionPoint,
    LeisureCenter,
    SportFacility,
    Randonnee,
    LieuTouristique, Hebergement, Gite,
    Commerce,
    Transport,
    AgencePostale,
    Mediatheque,
    MenuCantine,
    Defibrillateur,
    Signalement, SignalementPhoto,
)
from .serializers import (
    CommuneInfoSerializer,
    NewsSerializer,
    AssociationSerializer,
    HealthCenterSerializer,
    PharmacySerializer,
    SeniorResidenceSerializer,
    DefibrillateurSerializer,
    WasteCollectionScheduleSerializer, RecyclingCenterSerializer,
    GlassCollectionPointSerializer, TextileCollectionPointSerializer,
    LeisureCenterSerializer,
    SportFacilitySerializer,
    RandonneeSerializer,
    LieuTouristiqueSerializer, HebergementSerializer, GiteSerializer,
    CommerceSerializer,
    TransportSerializer,
    AgencePostaleSerializer,
    MediathequeSerializer,
    MenuCantineSerializer,
    SignalementCreateSerializer, SignalementSerializer,
)
from .permissions import HasMobileAPIKey


class SignalementThrottle(AnonRateThrottle):
    scope = 'signalement'


# ── Commune ──────────────────────────────────────────────────────────────────

@api_view(['GET'])
def commune_info(request):
    """Retourne les informations générales de la commune."""
    try:
        commune = CommuneInfo.objects.prefetch_related('horaires_planning').first()
        if not commune:
            return Response({'detail': 'Aucune information commune trouvée.'}, status=404)
        serializer = CommuneInfoSerializer(commune, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': str(e)}, status=500)


# ── Actualités ───────────────────────────────────────────────────────────────

class ActualiteListView(generics.ListAPIView):
    """Liste des actualités publiées, triées par date décroissante."""
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-event_date')

    def get_serializer_context(self):
        return {'request': self.request}


class ActualiteDetailView(generics.RetrieveAPIView):
    """Détail d'une actualité."""
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_published=True)

    def get_serializer_context(self):
        return {'request': self.request}


# ── Associations ─────────────────────────────────────────────────────────────

class AssociationListView(generics.ListAPIView):
    """Liste de toutes les associations."""
    serializer_class = AssociationSerializer
    queryset = Association.objects.all()

    def get_serializer_context(self):
        return {'request': self.request}


class AssociationDetailView(generics.RetrieveAPIView):
    """Détail d'une association."""
    serializer_class = AssociationSerializer
    queryset = Association.objects.all()
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {'request': self.request}


# ── Santé ────────────────────────────────────────────────────────────────────

@api_view(['GET'])
def sante(request):
    """Retourne toutes les données de santé (maisons de santé, pharmacies, résidences seniors)."""
    centres = HealthCenter.objects.prefetch_related('professionnels').all()
    pharmacies = Pharmacy.objects.prefetch_related('horaires_planning').all()
    residences = SeniorResidence.objects.all()

    return Response({
        'centres_sante': HealthCenterSerializer(centres, many=True, context={'request': request}).data,
        'pharmacies': PharmacySerializer(pharmacies, many=True, context={'request': request}).data,
        'residences_seniors': SeniorResidenceSerializer(residences, many=True, context={'request': request}).data,
    })


# ── Défibrillateurs ──────────────────────────────────────────────────────────

class DefibrillateurListView(generics.ListAPIView):
    """Liste des défibrillateurs actifs."""
    serializer_class = DefibrillateurSerializer
    queryset = Defibrillateur.objects.filter(est_actif=True)


# ── Déchets ──────────────────────────────────────────────────────────────────

@api_view(['GET'])
def dechets(request):
    """Retourne toutes les données de gestion des déchets."""
    planning = WasteCollectionSchedule.objects.all()
    dechetteries = RecyclingCenter.objects.prefetch_related('horaires').all()
    points_verre = GlassCollectionPoint.objects.all()
    points_textile = TextileCollectionPoint.objects.all()

    return Response({
        'planning_collecte': WasteCollectionScheduleSerializer(planning, many=True).data,
        'dechetteries': RecyclingCenterSerializer(dechetteries, many=True).data,
        'points_verre': GlassCollectionPointSerializer(points_verre, many=True).data,
        'points_textile': TextileCollectionPointSerializer(points_textile, many=True).data,
    })


# ── Loisirs ──────────────────────────────────────────────────────────────────

@api_view(['GET'])
def loisirs(request):
    """Retourne toutes les données de loisirs."""
    centre = LeisureCenter.objects.first()
    equipements = SportFacility.objects.select_related('type_equipement').all()
    randonnees = Randonnee.objects.all()

    return Response({
        'centre_loisirs': LeisureCenterSerializer(centre, context={'request': request}).data if centre else None,
        'equipements_sportifs': SportFacilitySerializer(equipements, many=True, context={'request': request}).data,
        'randonnees': RandonneeSerializer(randonnees, many=True, context={'request': request}).data,
    })


# ── Tourisme ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
def tourisme(request):
    """Retourne toutes les données touristiques."""
    lieux = LieuTouristique.objects.all()
    hebergements = Hebergement.objects.all()
    gites = Gite.objects.all()

    return Response({
        'lieux_touristiques': LieuTouristiqueSerializer(lieux, many=True, context={'request': request}).data,
        'hebergements': HebergementSerializer(hebergements, many=True, context={'request': request}).data,
        'gites': GiteSerializer(gites, many=True, context={'request': request}).data,
    })


# ── Infos pratiques ──────────────────────────────────────────────────────────

@api_view(['GET'])
def infos_pratiques(request):
    """Retourne toutes les informations pratiques."""
    commerces = Commerce.objects.prefetch_related('horaires').all()
    transports = Transport.objects.all()
    agence_postale = AgencePostale.objects.prefetch_related('horaires_planning').first()
    mediatheque = Mediatheque.objects.prefetch_related('horaires_planning').first()

    return Response({
        'commerces': CommerceSerializer(commerces, many=True).data,
        'transports': TransportSerializer(transports, many=True).data,
        'agence_postale': AgencePostaleSerializer(agence_postale).data if agence_postale else None,
        'mediatheque': MediathequeSerializer(mediatheque).data if mediatheque else None,
    })


# ── Menus Cantine ────────────────────────────────────────────────────────────

class MenuCantineListView(generics.ListAPIView):
    """Liste des menus de la cantine (10 dernières semaines)."""
    serializer_class = MenuCantineSerializer

    def get_queryset(self):
        return MenuCantine.objects.all()[:10]

    def get_serializer_context(self):
        return {'request': self.request}


# ── Signalement ──────────────────────────────────────────────────────────────

class SignalementCreateView(APIView):
    """
    Crée un signalement depuis l'app mobile.
    Accepte des photos en multipart/form-data.
    Nécessite la clé API mobile dans le header X-Api-Key.
    """
    permission_classes = [HasMobileAPIKey]
    throttle_classes = [SignalementThrottle]

    def post(self, request):
        serializer = SignalementCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        signalement = serializer.save()

        # Gestion des photos (jusqu'à 5 photos)
        photos = request.FILES.getlist('photos')
        for i, photo in enumerate(photos[:5]):
            SignalementPhoto.objects.create(
                signalement=signalement,
                image=photo,
                order=i
            )

        # Notification par email à la mairie
        try:
            from core.models import CommuneInfo
            commune = CommuneInfo.objects.first()
            destinataire = commune.email if commune else settings.BREVO_RECIPIENT_EMAIL

            localisation = ''
            if signalement.latitude and signalement.longitude:
                localisation = f'\nLocalisation GPS : https://maps.google.com/?q={signalement.latitude},{signalement.longitude}'
            if signalement.adresse_approximative:
                localisation += f'\nAdresse : {signalement.adresse_approximative}'

            send_mail(
                subject=f'[Signalement] {signalement.get_categorie_display()} — Application mobile',
                message=(
                    f'Un habitant a soumis un signalement via l\'application mobile.\n\n'
                    f'Catégorie : {signalement.get_categorie_display()}\n'
                    f'Description : {signalement.description}'
                    f'{localisation}\n'
                    f'Email signalant : {signalement.email_signalant or "Non renseigné"}\n'
                    f'Nombre de photos : {len(photos)}\n'
                    f'Date : {signalement.created_at.strftime("%d/%m/%Y %H:%M")}'
                ),
                from_email=settings.BREVO_SENDER_EMAIL,
                recipient_list=[destinataire],
                fail_silently=True,
            )
        except Exception:
            pass  # L'email est non bloquant

        return Response(
            SignalementSerializer(signalement, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
