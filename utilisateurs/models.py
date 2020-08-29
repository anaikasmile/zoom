#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from agences.models import Agences
from django.core.validators import RegexValidator

class User(AbstractUser):
    # USER_TYPE_CHOICES = (
    #     (1, 'admin'),
    #     (2, 'agent'),
    #     (3, 'chauffeur'),
    # )
    SEXE = (
        (u'F', _(u'Feminin')),
        (u'M', _(u'Masculin')),
    )

    #user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True, blank=True)
    sexe = models.CharField(max_length=10, choices=SEXE)
    adresse = models.TextField(max_length=500, blank=True, verbose_name="Adresse")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Date de naissance", help_text=_(u'JJ/MM/AAAA'))
    tel = PhoneNumberField(max_length=50, unique=True, verbose_name=_(u'Téléphone'), help_text=_(u'+228________'))
    photo = models.ImageField(upload_to="utilisateurs", blank=True, null=True)

    #TEL_FIELD = 'tel'
    def __str__(self):
        return self.last_name+' '+self.first_name


    def get_full_name(self):
        return self.first_name+' '+self.last_name
#
# Create your models here.
class Person(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name ='person')
    job = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession")
    is_client = models.BooleanField(default=True)

   

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    # @receiver(post_save, sender=User)
    # def create_or_update_user_person(sender, instance, created, **kwargs):
    #     if created:
    #         Person.objects.create(user=instance)
    #     instance.person.save()


class Agent(models.Model):
    TYPE = (
        (u'CNI', _(u'Carte Nationale d Identité')),
        (u'Passeport', _(u'Passeport')),
        (u'Permis', _(u'Permis de conduire')),

    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name ='agent')
    agence  = models.ForeignKey(Agences, related_name='agent', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE)
    reference = models.CharField(max_length=50, verbose_name=_(u'N° matricule'))
    photo = models.ImageField(upload_to="pieces_identites", blank=True, null=True)
    initiated_at = models.DateField(verbose_name=_(u'Emis le'))
    expired_at = models.DateField(verbose_name=_(u'Expire le'))
    contact_name = models.CharField(max_length=50, verbose_name=_(u'Nom'), blank=True)
    contact_tel = models.CharField(max_length=50, verbose_name=_(u'Tél'), blank=True, help_text=_(u''))
    is_agent = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

   

class Identity(models.Model):
    TYPE = (
        (u'CNI', _(u'Carte Nationale d Identité')),
        (u'Passeport', _(u'Passeport')),
        (u'Permis', _(u'Permis de conduire')),

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='identites', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE)
    reference = models.CharField(max_length=50, verbose_name=_(u'N° matricule'))
    photo = models.ImageField(upload_to="pieces_identites", blank=True, null=True)
    initiated_at = models.DateField(verbose_name=_(u'Emis le'))
    expired_at = models.DateField(verbose_name=_(u'Expire le'))
    contact_name = models.CharField(max_length=50, verbose_name=_(u'Nom'), blank=True)
    contact_tel = models.CharField(max_length=50, verbose_name=_(u'Tél'), blank=True, help_text=_(u''))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.reference
