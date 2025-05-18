from django.contrib import admin
from django.utils.html import format_html

from .models import  Commande,ProduitCommande




class ProduitCommandeInline(admin.TabularInline):
    model = ProduitCommande
    extra = 1

class CommandeAdmin(admin.ModelAdmin):
    inlines = [ProduitCommandeInline]
    list_display = ('id', 'nom_client', 'produits_commandes','date_commande','adresse','telephone','montant_total')

    def produits_commandes(self, obj):
        produits = ProduitCommande.objects.filter(commande=obj)  # Récupérer tous les produits de la commande
        return format_html(
            "<br>".join([f"{produit.produit.nom} (Quantité: {produit.quantite})" for produit in produits])
        )

    produits_commandes.short_description = "Produits Commandés"

admin.site.register(Commande,CommandeAdmin)

