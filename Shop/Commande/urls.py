
from django.urls import path

from . import views

urlpatterns = [
    path('panier/', views.vue_panier, name='vue_panier'),
    path('supprimer-panier/', views.supprimer_panier, name='supprimer_panier'),
    path('enregistrer-commande/', views.enregistrer_commande, name='enregistrer_commande'),
    path('show_video/<str:slug>/', views.show_video, name='produit'),
    path('commande/<str:slug>/', views.single_commande, name='commande'),
    path('video-finished/', views.mark_video_finished, name='video_finished'),
    path('ajouter_avis/<str:slug>/', views.ajout_avis, name='ajouter_avis'),
]
