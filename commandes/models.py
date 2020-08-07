from django.db import models
from geolocalisation.models import City
from utilisateurs.models import User
from agences.models import Agences
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
from datetime import datetime



# Create your models here.
class Colis(models.Model):
    client = models.ForeignKey(User, null=True, related_name='client', on_delete=models.CASCADE)
    nature = models.CharField(max_length=200, verbose_name='Nature', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(blank=True,null=True, upload_to="colis")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, verbose_name="Poids")
    size = models.CharField(max_length=100, blank=True, verbose_name="Taille")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Modifié le")
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


class Package(models.Model):
    libelle = models.CharField(max_length=50, null=True, blank=True, verbose_name='Libelle')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Modifié le")
    def __str__(self):
        return self.libelle


class Commandes(models.Model):
    ETAT_NON_ACCEPTE = 0

    ETAT_ACCEPTE = 1

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
    numero_commande = models.CharField(max_length=200, verbose_name='N° Commande', null=True, blank=True)

    colis = models.OneToOneField(Colis, related_name='colis', on_delete=models.CASCADE, verbose_name="Nature du colis")
    insurance = models.ForeignKey(Insurance, null=True, related_name='insurance', verbose_name="Assurance", on_delete=models.CASCADE)
    city_depart = models.ForeignKey(City, null=True, related_name='cityDepart', verbose_name="Ville de départ", on_delete=models.CASCADE)
    city_arrive = models.ForeignKey(City, null=True, related_name='cityArrival', verbose_name="Ville d'arrivée", on_delete=models.CASCADE)
    date_depot = models.DateField(null=True, blank=True, verbose_name="Date de dépot")
    date_reception = models.DateField(null=True, blank=True, verbose_name="Date de réception")
    observation = models.TextField(null=True, blank=True, verbose_name="Remarques")
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, verbose_name="Prix")
    commission = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True, verbose_name="Commission")
    status = models.PositiveSmallIntegerField(null=True, blank=True, default=ETAT_NON_PAYE, verbose_name="Etat")
    accepted = models.PositiveSmallIntegerField(null=True, blank=True, default=ETAT_NON_ACCEPTE, verbose_name="Accepté")

    package = models.ForeignKey(Package, verbose_name="Package d'envoi", on_delete=models.CASCADE)
    driver = models.ForeignKey(User, null=True, related_name='commandes_drivers', on_delete=models.CASCADE, verbose_name="Conducteur")
    agent = models.ForeignKey(User, null=True, related_name='commandes_agent', on_delete=models.CASCADE, verbose_name="Agent")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Modifié le")

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

    def getAcceptedLibelle(self):
        if self.accepted == self.ETAT_NON_ACCEPTE:
            libelle = "Non"

        elif self.accepted == self.ETAT_ACCEPTE:
            libelle = "Oui"
        else:
            libelle = ""
        return libelle

    def getTrancheData(colis):
        #tranches = Tranche.objects.all()
        data = 0.00
        # data = {
        #     "amount": 0.00,
        #     "commission": 0.00
        # }
        # for t in tranches:
        #     minimum = colis.weight
        #     if colis.weight >= t.min_weight and colis.weight  <= t.max_weight:
        #         data = {
        #            "amount": t.price,
        #            "commission":  t.commission
        #         }
        return data


class Facture(models.Model):
    ETAT = (
        ('Non payé', 'Non payé'),
        ('Payé', 'Payé'),

    )
    commande = models.ForeignKey(Commandes, related_name='commandeFacture', on_delete=models.CASCADE)
    reference = models.CharField(max_length=50, verbose_name='Référence')
    status = models.CharField(null=True, blank=True, choices=ETAT, verbose_name="Etat", max_length=15)
    link_facture = models.CharField (max_length=50, null=True, blank=True, verbose_name='Lien facture')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        now = datetime.now()

        self.reference = now.strftime("%d%m%Y")+'_'+''.join(random.choice(string.ascii_uppercase) for _ in range(5))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.reference
    
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

     @property
     def sorted_historique(self):
         return self.sorted_historique.order_by('-created_at')



class Reclamations(models.Model):
    TYPES = (
        ('Endommagé', 'Endommagé'),
        ('Perdu', 'Perdu'),
        ('Délai dépassé', 'Délai dépassé'),

    )
    commande = models.ForeignKey(Commandes, related_name='commandeIncident', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True,verbose_name="Mis à jour le")
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
    type = models.CharField(max_length=50, choices=TYPES, null=True, blank=True, verbose_name='Action faite')
    commentaire = models.TextField(blank=True, verbose_name='Commentaire')




class Tranche(models.Model):
    min_weight = models.IntegerField(verbose_name="Minimum")
    max_weight = models.IntegerField(verbose_name="Maximum")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix")
    package = models.ForeignKey(Package,related_name='packageTranche', verbose_name="Package d'envoi", on_delete=models.CASCADE)
    commission = models.DecimalField(max_digits=5, decimal_places=2,verbose_name="Commission")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        """docstring for Meta"""
        constraints = [
                models.UniqueConstraint(fields=['package', 'min_weight', 'max_weight', 'price'], name='tranche_unique')
            ]
    #def __str__(self):
    #   return self.min_weight