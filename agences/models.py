from django.db import models
from geolocalisation.models import District
# Create your models here.
class Agences(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom *")
    district = models.ForeignKey(District, verbose_name="Quartier *", null=True, on_delete=models.PROTECT)

    addresses = models.TextField(null=True, blank=True, verbose_name="Adresse")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    def __str__(self):
        return self.name




class Societe(models.Model):
    district = models.ForeignKey(District, verbose_name="Quartier *", null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, verbose_name="Nom *")
    addresses = models.TextField(null=True, blank=True, verbose_name="Adresse")
    tel = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tél")
    email = models.CharField(max_length=200, blank=True, null=True, verbose_name="Email")

    logo = models.ImageField(blank=True,null=True, upload_to="agences")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    def __str__(self):
        return self.name