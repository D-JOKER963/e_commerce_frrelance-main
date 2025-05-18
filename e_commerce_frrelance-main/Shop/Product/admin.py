from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms


class ProduitAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Produit
        fields = '__all__'


class ImageProduitInline(admin.TabularInline):
    model = ImageProduit
    extra = 1


class ProduitAdmin(admin.ModelAdmin):
    form = ProduitAdminForm
    inlines = [ImageProduitInline]
    list_display = ('nom', 'categorie', 'prix')
    readonly_fields = ('slug',)

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('libelle')

admin.site.register(Avis)
admin.site.register(Categorie)
admin.site.register(Produit,ProduitAdmin)
