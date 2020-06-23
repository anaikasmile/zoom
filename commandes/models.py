from django.db import models
from geolocalisation.models import City
from utilisateurs.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string

# Create your models here.
class Colis(models.Model):
    client = models.ForeignKey(User, null=True, related_name='client', on_delete=models.CASCADE)
    nature = models.CharField(max_length=200, verbose_name='Nature', null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(blank=True,null=True)
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
    ETAT_CMD = (
        (1, 'Non payé'),
        (2, 'Payé'),
        (3, 'En transit'),
        (4, 'Livré'),
    )

    MODELE_ENVOI = (
        ('VIP', 'VIP'),
        ('STANDARD', 'STANDARD'),
        ('PREMIUM', 'PREMIUM'),

    )
    numero_commande = models.CharField(max_length=200, verbose_name='Réference', null=True, blank=True)
    colis = models.OneToOneField(Colis, related_name='colis', on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, null=True, related_name='insurance', on_delete=models.CASCADE)
    city_depart = models.ForeignKey(City, null=True, related_name='cityDepart', on_delete=models.CASCADE)
    city_arrive = models.ForeignKey(City, null=True, related_name='cityArrival', on_delete=models.CASCADE)
    date_depot = models.DateField(null=True, blank=True)
    date_reception = models.DateField(null=True, blank=True)
    observation = models.TextField(null=True, blank=True, verbose_name="Remarques")
    price = models.FloatField(null=True, blank=True, verbose_name="Prix")
    status = models.PositiveSmallIntegerField(choices=ETAT_CMD, null=True, blank=True)
    modele = models.CharField(max_length=50,choices=MODELE_ENVOI, null=True, blank=True, verbose_name='Modèle envoi')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return self.colis.nature



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