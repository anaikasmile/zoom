from django.db import models
from django_countries.fields import CountryField


# Create your models here.
class City(models.Model):
    country = CountryField(blank_label=('Choisissez le pays'), blank=True, null=True, verbose_name="Pays *")
    name = models.CharField(verbose_name="Nom *", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    def __str__(self):
        return self.name

class District(models.Model):
    city = models.ForeignKey(City, related_name='district', verbose_name="Ville *", on_delete=models.PROTECT)
    name = models.CharField(max_length=200, verbose_name="Nom *")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    def __str__(self):
        return self.name
