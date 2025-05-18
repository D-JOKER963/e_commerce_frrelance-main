from datetime import datetime

from django.db import models

from Product.models import Produit

class Commande(models.Model):
    nom_client = models.CharField(max_length=100)
    telephone = models.CharField(max_length=10)
    adresse = models.CharField(max_length=150)
    date_commande = models.DateTimeField(auto_now_add=True)
    montant_total = models.PositiveIntegerField(default=0)

class ProduitCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    montant = models.PositiveIntegerField(default=0)


