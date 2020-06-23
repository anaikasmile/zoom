#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Agences,  TypeVehicules, Vehicules

from django.utils.translation import ugettext_lazy as _

class AgenceForm(forms.ModelForm):
    class Meta:
        model = Agences
        fields = ('name', 'district', 'addresses')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'district': forms.Select(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'addresses': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
             }

class TypeVehiculeForm(forms.ModelForm):
    class Meta:
        model = TypeVehicules
        fields = ('libelle', )
        widgets = {
                'libelle': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
                }

class VehiculesForm(forms.ModelForm):
    class Meta:
        model = Vehicules
        fields = ('user', 'immatriculation', 'marque', 'modele', 'etat', 'type', 'description','nb_place' )
        widgets = {
            'user': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'immatriculation': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'marque':  forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'modele': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'etat': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'nb_place': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
        }