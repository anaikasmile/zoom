from django.db import models
from geolocalisation.models import District
from utilisateurs.models import User
# Create your models here.
class Agences(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom *")
    district = models.ForeignKey(District, verbose_name="Quartier *", null=True, on_delete=models.PROTECT)

    addresses = models.TextField(null=True, blank=True, verbose_name="Adresse")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    def __str__(self):
        return self.name

class TypeVehicules(models.Model):
    libelle = models.CharField(max_length=200, verbose_name='Type')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.libelle


class Vehicules(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Chauffeur')
    type = models.ForeignKey(TypeVehicules, on_delete=models.PROTECT, verbose_name='Type de véhicules *')
    marque = models.CharField(max_length=200, verbose_name='Marque',  blank=True, null=True)
    modele = models.CharField(max_length=200, verbose_name='Modèle',  blank=True, null=True)
    immatriculation = models.CharField(max_length=200, verbose_name='immatriculation *', null=True, blank=True)
    nb_place = models.IntegerField(verbose_name='Nombre de places', blank=True, null=True)
    etat = models.TextField(blank=True, verbose_name="Etat du véhicule", null=True)
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    # image = models.ImageField(blank=True,null=True, upload_to="vehicules")
    # pieceIdentification = models.ImageField(blank=True,null=True, upload_to="vehicules")


    def __str__(self):
        return self.immatriculation


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