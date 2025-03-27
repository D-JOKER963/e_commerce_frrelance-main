from django.contrib import admin
from .models import *



class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 1


class ProduitAdmin(admin.ModelAdmin):
    inlines = [ImageProduitInline]
    list_display = ('nom', 'categorie', 'prix')
    readonly_fields = ('slug',)

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('libelle')

admin.site.register(Avis)
admin.site.register(Categorie)
admin.site.register(Produit,ProduitAdmin)
