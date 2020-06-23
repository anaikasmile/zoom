#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Colis, Insurance, Commandes
from django.forms.models import inlineformset_factory



from django.utils.translation import ugettext_lazy as _

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ('nom', 'assureur', 'taux')
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'assureur': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'taux': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
             }

class ColisForm(forms.ModelForm):
    class Meta:
        model = Colis
        fields = ('nature', 'weight', 'description', 'image','size')
        widgets = {
            'nature': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'weight': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'size': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

            'description': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'image': forms.FileInput(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'custom-file-input'}),
        }

class CommandesForm(forms.ModelForm):
    class Meta:
        model = Commandes
        fields = ('numero_commande', 'city_depart', 'city_arrive', 'date_depot', 'date_reception', 'price', 'modele',
                  'colis', 'insurance', 'observation', 'status')
        widgets = {
            'numero_commande': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'colis': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'insurance': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_arrive': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_depart': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_depot': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date','placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_reception': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'modele': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'required': False, 'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'status': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

        }

CommandesFormset = inlineformset_factory(
    Colis, Commandes,
    fields=('city_depart', 'city_arrive', 'date_depot', 'date_reception', 'modele',
                   'insurance'),
    widgets = {
            #'numero_commande': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
           # 'colis': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'insurance': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_arrive': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_depart': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_depot': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date','placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_reception': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'modele': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            #'weight': forms.NumberInput(attrs={'required': False, 'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            #'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            #'price': forms.NumberInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            #'status': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

        }
    )
