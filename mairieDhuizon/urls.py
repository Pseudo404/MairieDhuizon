from django.contrib import admin
from django.urls import path
from core import views, centre_loisirs_views, centre_loisirs_admin_views

urlpatterns = [
    path('', views.home, name='home'),
    path('decouvrir-dhuizon/', views.decouvrir_dhuizon, name='decouvrir_dhuizon'),
    path('vie-pratique/', views.vie_pratique, name='vie_pratique'),
    path('loisirs/', views.loisirs, name='loisirs'),
    path('loisirs/randonnees/<slug:slug>/', views.randonnee_detail, name='randonnee_detail'),
    path('demarches/', views.demarches, name='demarches'),
    path('etat-civil/', views.etat_civil, name='etat_civil'),
    path('tourisme/', views.tourisme, name='tourisme'),
    path('entreprises/', views.entreprises, name='entreprises'),
    path('actualite/<int:news_id>/', views.actualite_detail, name='actualite_detail'),
    path('contact/', views.contact, name='contact'),
    path('conseil-municipal/', views.conseil_municipal, name='conseil_municipal'),
    path('vie-associative/', views.vie_associative, name='vie_associative'),
    path('vie-associative/<slug:slug>/', views.association_detail, name='association_detail'),
    path('fichiers/<path:relative_path>', views.serve_upload, name='serve_upload'),
    # Rétrocompatibilité : anciens liens /media/ (admin Django, favoris…)
    path('media/<path:relative_path>', views.serve_upload, name='serve_media_legacy'),
    path('control-panel/', views.control_panel, name='control_panel'),
    path('control-panel/parametres/', views.admin_settings, name='admin_settings'),
    path('control-panel/manage/<str:app_label>/<str:model_name>/', views.panel_crud_list, name='panel_crud_list'),
    path('control-panel/manage/<str:app_label>/<str:model_name>/add/', views.panel_crud_form, name='panel_crud_add'),
    path('control-panel/manage/<str:app_label>/<str:model_name>/<int:pk>/edit/', views.panel_crud_form, name='panel_crud_edit'),
    path('control-panel/manage/<str:app_label>/<str:model_name>/<int:pk>/delete/', views.panel_crud_delete, name='panel_crud_delete'),
    path('control-panel/manage/<str:app_label>/<str:model_name>/<int:pk>/toggle-publish/', views.panel_crud_toggle_publish, name='panel_crud_toggle_publish'),
    path('too-many-requests/', views.too_many_requests, name='too_many_requests'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('logout-admin/', views.logout_admin, name='logout_admin'),
    path('control-panel/stats/', views.admin_stats, name='admin_stats'),
    path('control-panel/logs/', views.admin_audit_logs, name='admin_audit_logs'),
    path('api/realtime-count/', views.api_realtime_count, name='api_realtime_count'),
    path('api/track-time/', views.api_track_time, name='api_track_time'),
    path('api/export-csv/', views.api_export_csv, name='api_export_csv'),
    path('recherche/', views.vue_recherche, name='recherche'),
    path('politique-confidentialite/', views.politique_confidentialite, name='politique_confidentialite'),
    path('inscription-periscolaire/', views.inscription_periscolaire, name='inscription_periscolaire'),

    path('centre-loisirs/inscription/', centre_loisirs_views.centre_loisirs_choix_dates, name='centre_loisirs_inscription'),
    path('centre-loisirs/inscription/formulaire/', centre_loisirs_views.centre_loisirs_formulaire, name='centre_loisirs_formulaire'),
    path('centre-loisirs/reservation/<uuid:token>/', centre_loisirs_views.centre_loisirs_reservation, name='centre_loisirs_reservation'),
    path('centre-loisirs/confirmation/<uuid:token>/', centre_loisirs_views.centre_loisirs_confirmation, name='centre_loisirs_confirmation'),
    path('centre-loisirs/annulation/<uuid:token>/', centre_loisirs_views.centre_loisirs_annulation, name='centre_loisirs_annulation'),
    path('api/calendrier-loisirs/', centre_loisirs_views.api_calendrier_data, name='api_calendrier_data'),
    
    path('control-panel/centre-loisirs/', centre_loisirs_admin_views.admin_cl_dashboard, name='admin_cl_dashboard'),
    path('control-panel/centre-loisirs/reservations/', centre_loisirs_admin_views.admin_cl_reservations, name='admin_cl_reservations'),
    path('control-panel/centre-loisirs/reservations/<int:pk>/valider/', centre_loisirs_admin_views.admin_cl_valider_reservation, name='admin_cl_valider_reservation'),
    path('control-panel/centre-loisirs/reservations/<int:pk>/refuser/', centre_loisirs_admin_views.admin_cl_refuser_reservation, name='admin_cl_refuser_reservation'),
    path('control-panel/centre-loisirs/reservations/<int:pk>/supprimer/', centre_loisirs_admin_views.admin_cl_supprimer_reservation, name='admin_cl_supprimer_reservation'),
    path('control-panel/centre-loisirs/jours/', centre_loisirs_admin_views.admin_cl_gestion_jours, name='admin_cl_gestion_jours'),
    path('control-panel/centre-loisirs/historique/', centre_loisirs_admin_views.admin_cl_historique, name='admin_cl_historique'),
    path('control-panel/centre-loisirs/jours/<str:date>/', centre_loisirs_admin_views.admin_cl_detail_jour, name='admin_cl_detail_jour'),
    path('control-panel/centre-loisirs/calendrier/', centre_loisirs_admin_views.admin_cl_calendrier, name='admin_cl_calendrier'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
