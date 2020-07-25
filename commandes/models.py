from django.db import models
from geolocalisation.models import City
from utilisateurs.models import User
from agences.models import Agences
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string

# Create your models here.
class Colis(models.Model):
    client = models.ForeignKey(User, null=True, related_name='client', on_delete=models.CASCADE)
    nature = models.CharField(max_length=200, verbose_name='Nature', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(blank=True,null=True, upload_to="colis")
    weight = models.FloatField(blank=True, verbose_name="Poids")
    size = models.CharField(max_length=100, blank=True, verbose_name="Taille")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.nature

class Insurance(models.Model):
    nom = models.CharField(max_length=200, verbose_name='Nom', null=True, blank=True)
    assureur = models.CharField(max_length=200, verbose_name='Assureur', null=True, blank=True)
    taux = models.FloatField(verbose_name='Taux', null=True, blank=True)
    start_at = models.DateField(null=True, blank=True)
    end_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    def __str__(self):
        return self.nom

class Commandes(models.Model):
    ETAT_NON_PAYE = 1
    ETAT_PAYE = 2
    ETAT_EN_TRANSIT = 3
    ETAT_EN_AGENCE = 4
    ETAT_LIVRE = 5
    ETAT_RECEPTIONNE = 6

    MODELE_ENVOI = (
        ('VIP', 'VIP'),
        ('STANDARD', 'STANDARD'),
        ('PREMIUM', 'PREMIUM'),

    )
    numero_commande = models.CharField(max_length=200, verbose_name='Réference', null=True, blank=True)
    driver = models.ForeignKey(User, null=True, related_name='commandes_drivers', on_delete=models.CASCADE)

    colis = models.OneToOneField(Colis, related_name='colis', on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, null=True, related_name='insurance', on_delete=models.CASCADE)
    city_depart = models.ForeignKey(City, null=True, related_name='cityDepart', on_delete=models.CASCADE)
    city_arrive = models.ForeignKey(City, null=True, related_name='cityArrival', on_delete=models.CASCADE)
    date_depot = models.DateField(null=True, blank=True)
    date_reception = models.DateField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True, verbose_name="Remarques")
    price = models.FloatField(null=True, blank=True, verbose_name="Prix")
    #commission = models.FloatField(null=True, blank=True, verbose_name="Commission")
    status = models.PositiveSmallIntegerField(null=True, blank=True, default=ETAT_NON_PAYE)
    modele = models.CharField(max_length=50, choices=MODELE_ENVOI, null=True, blank=True, verbose_name='Modèle envoi')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def create_ref_code(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits, k=20))

    def save(self, *args, **kwargs):
        self.numero_commande = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        super().save(*args, **kwargs)
    def __str__(self):
        return self.numero_commande

    def getEtatLibelle(self):
        if self.status == self.ETAT_NON_PAYE:
            libelle = "Non payé"

        elif self.status == self.ETAT_PAYE:
            libelle = "Payé"
        elif self.status == self.ETAT_EN_AGENCE:
            libelle = "Dépôt en agence"
        elif self.status == self.ETAT_RECEPTIONNE:
            libelle = "Réceptionné"
        elif self.status == self.ETAT_LIVRE:
            libelle = "Livré"
        elif self.status == self.ETAT_EN_TRANSIT:
            libelle = "En transit"
        else:
            libelle = ""
        return libelle



    # def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    #     return ''.join(random.choice(chars) for _ in range(size))
    #
    # def unique_order_id_generator(instance):
    #     order_new_id = random_string_generator()
    #
    #     Klass = instance.__class__
    #
    #     qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    #     if qs_exists:
    #         return unique_order_id_generator(instance)
    #     return order_new_id

class HistoriqueCommandes(models.Model):
     ETAT_NON_PAYE = 1
     ETAT_PAYE = 2
     ETAT_EN_TRANSIT = 3
     ETAT_EN_AGENCE = 4
     ETAT_LIVRE = 5
     ETAT_RECEPTIONNE = 6

     user = models.ForeignKey(User, related_name='userHistorique', on_delete=models.CASCADE)
     commande = models.ForeignKey(Commandes, related_name='commandeHistorique', on_delete=models.CASCADE)
     agence  = models.ForeignKey(Agences, null=True, related_name='agenceHistorique', on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
     updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
     state = models.PositiveSmallIntegerField()
     comment = models.TextField(null=True, blank=True, verbose_name="Commentaire")

     def getEtatLibelle(self):
         if self.state == self.ETAT_NON_PAYE:
             libelle = "Non payé"
         if self.state == self.ETAT_PAYE:
             libelle = "Payé"
         if self.state == self.ETAT_EN_AGENCE:
             libelle = "Dépôt en agence"
         if self.state == self.ETAT_RECEPTIONNE:
             libelle = "Réceptionné"
         if self.state == self.ETAT_LIVRE:
             libelle = "Livré"
         if self.state == self.ETAT_EN_TRANSIT:
             libelle = "En transit"
         return libelle

     def __str__(self):
         return self.commande.numero_commande+" "+self.getEtatLibelle()


class Reclamations(models.Model):
    TYPES = (
        ('Endommagé', 'Endommagé'),
        ('Perdu', 'Perdu'),
        ('Délai dépassé', 'Délai dépassé'),

    )
    commande = models.ForeignKey(Commandes, related_name='commandeIncident', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPES, null=True, blank=True, verbose_name='Type d incident')
    observation = models.TextField(blank=True, verbose_name='Observations')
    image = models.ImageField(blank=True, null=True, upload_to="reclamations")

    def __str__(self):
        return self.commande.numero_commande

class ReclamationsHandler(models.Model):
    TYPES = (
        ('En cours de traitement', 'En cours de traitement'),
        ('Résolu', 'Résolu'),
        ('Non résolu', 'Non résolu'),

    )
    reclamation = models.ForeignKey(Reclamations, related_name='reclamationHandler', on_delete=models.CASCADE)
    agent = models.ForeignKey(User,related_name='userReclamations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPES, null=True, blank=True, verbose_name='Type d incident')
    commentaire = models.TextField(blank=True, verbose_name='Commentaire')


class Tranche(models.Model):
    min_weight = models.FloatField(verbose_name="Minimum")
    max_weight = models.FloatField(verbose_name="Maximum")
    price = models.FloatField(verbose_name="Prix")
    commission = models.FloatField(verbose_name="Commission", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        """docstring for Meta"""
        constraints = [
                models.UniqueConstraint(fields=['min_weight', 'max_weight', 'price'], name='tranche_unique')
            ]