"""
permissions.py — Permissions personnalisées pour l'API mobile.
"""
from rest_framework.permissions import BasePermission
from django.conf import settings


class HasMobileAPIKey(BasePermission):
    """
    Permission qui vérifie la présence d'une clé API dans le header
    X-API-Key. Utilisée pour les endpoints d'écriture (signalements).
    """
    message = "Clé API mobile manquante ou invalide."

    def has_permission(self, request, view):
        api_key = request.headers.get('X-Api-Key', '')
        return api_key == settings.MOBILE_API_KEY
