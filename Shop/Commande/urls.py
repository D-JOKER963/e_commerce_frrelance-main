
from django.urls import path

from Commande import views

urlpatterns = [
    path('panier/', views.vue_panier, name='vue_panier'),
    path('supprimer-panier/', views.supprimer_panier, name='supprimer_panier'),
    path('enregistrer-commande/', views.enregistrer_commande, name='enregistrer_commande'),
]
