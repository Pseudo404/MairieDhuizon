"""
urls.py — Routes de l'API REST mobile /api/v1/
"""
from django.urls import path
from . import views

urlpatterns = [
    # Commune
    path('commune/', views.commune_info, name='api-commune'),

    # Actualités
    path('actualites/', views.ActualiteListView.as_view(), name='api-actualites'),
    path('actualites/<int:pk>/', views.ActualiteDetailView.as_view(), name='api-actualite-detail'),

    # Associations
    path('associations/', views.AssociationListView.as_view(), name='api-associations'),
    path('associations/<slug:slug>/', views.AssociationDetailView.as_view(), name='api-association-detail'),

    # Santé
    path('sante/', views.sante, name='api-sante'),
    path('defibrillateurs/', views.DefibrillateurListView.as_view(), name='api-defibrillateurs'),

    # Déchets
    path('dechets/', views.dechets, name='api-dechets'),

    # Loisirs
    path('loisirs/', views.loisirs, name='api-loisirs'),

    # Tourisme
    path('tourisme/', views.tourisme, name='api-tourisme'),

    # Infos pratiques
    path('infos-pratiques/', views.infos_pratiques, name='api-infos-pratiques'),

    # Menus cantine
    path('menus-cantine/', views.MenuCantineListView.as_view(), name='api-menus-cantine'),

    # Signalement
    path('signalements/', views.SignalementCreateView.as_view(), name='api-signalement-create'),
]
