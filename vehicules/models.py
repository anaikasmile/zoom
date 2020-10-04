from django.db import models
from utilisateurs.models import User

# Create your models here.
class TypeVehicules(models.Model):
    libelle = models.CharField(max_length=200, verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.libelle


class Vehicules(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='vehicules', verbose_name='Chauffeur')
    type = models.ForeignKey(TypeVehicules, on_delete=models.PROTECT, verbose_name='Type *')
    marque = models.CharField(max_length=200, verbose_name='Marque',  blank=True, null=True)
    modele = models.CharField(max_length=200, verbose_name='Modèle',  blank=True, null=True)
    immatriculation = models.CharField(max_length=200, verbose_name='immatriculation *', null=True, blank=True)
    nb_place = models.IntegerField(verbose_name='Nb places', blank=True, null=True)
    etat = models.TextField(blank=True, verbose_name="Etat", null=True)
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    image = models.ImageField(blank=True,null=True, upload_to="vehicules")
    # pieceIdentification = models.ImageField(blank=True,null=True, upload_to="vehicules")

    def __str__(self):
        return self.immatriculation