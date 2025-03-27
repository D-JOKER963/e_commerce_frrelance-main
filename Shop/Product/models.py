from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Categorie(models.Model):
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Produit(models.Model):
    categorie = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    nom = models.CharField(max_length=120)
    slug = models.SlugField(max_length=50,blank=True)
    description = models.TextField(blank=True)
    ancien_prix = models.PositiveIntegerField(default=0,null=True,blank=True)
    prix = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('produit', kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Produit, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom}"


class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True, upload_to="images/")
    video_desc = models.FileField(blank=True,null=True, upload_to="videos/")