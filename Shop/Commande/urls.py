
from django.urls import path

from Commande import views

urlpatterns = [
    path('', views.vue_panier, name='vue_panier'),
]
