#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Colis, Insurance, Commandes, Reclamations, ReclamationsHandler, Tranche, Package
from agences.models import Agences
from django.forms.models import inlineformset_factory
from django.forms import ModelChoiceField



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
            'image': forms.FileInput(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input','lang' :'fr'}),
        }

class CommandesForm(forms.ModelForm):
    class Meta:
        model = Commandes
        fields = ('numero_commande', 'city_depart', 'city_arrive', 'date_depot', 'date_reception', 'price', 'package',
                  'colis', 'insurance', 'observation', 'status')
        widgets = {
            'numero_commande': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'colis': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'insurance': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_arrive': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_depart': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_depot': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date','placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_reception': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'package': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'required': True, 'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'status': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

        }

class CommandesSetForm(forms.ModelForm):
    class Meta:
        model = Commandes
        fields = ('city_depart', 'city_arrive', 'date_depot', 'date_reception', 'price', 'package',
                   'insurance', 'observation')
        widgets = {
            'insurance': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_arrive': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_depart': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_depot': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date','placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_reception': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'package': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'required': True, 'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),

        }

CommandesFormSet = inlineformset_factory(
    Colis, Commandes, fk_name='colis',
    fields=('city_depart', 'city_arrive', 'date_depot', 'date_reception', 'package', 'insurance'),
    widgets = {
            'insurance': forms.Select(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_arrive': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'city_depart': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_depot': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date','placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'date_reception': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'package': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            #'weight': forms.NumberInput(attrs={'required': False, 'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            #'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            #'price': forms.NumberInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            #'status': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

        },can_delete = False, extra=1
    )



class Step1Form(forms.Form):
    ETAT_CMD = (
        (1, 'Non payé'),
        (2, 'Payé'),
        (3, 'En transit'),
        (4, 'En agence'),
        (5, 'Livré'),
    )
    etat = forms.ChoiceField(choices = ETAT_CMD,widget=forms.Select(attrs={'class': 'form-control'}))

class Step2Form(forms.Form):
    agence = forms.ModelChoiceField(queryset=Agences.objects.all(), initial=0, widget=forms.Select(attrs={'class': 'form-control'}))
    commentaire = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))


class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamations
        fields = ('commande', 'type', 'observation', 'image')
        widgets = {
            'commande': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'image': forms.FileInput(attrs={'required': False, 'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input','lang' :'fr'}),
        }
    def __init__(self, user, *args, **kwargs):
        super(ReclamationForm, self).__init__(*args, **kwargs)
        self.fields['commande'].queryset = Commandes.objects.filter(colis__client=user)

class ReclamationHandlerForm(forms.ModelForm):
    class Meta:
        model = ReclamationsHandler
        fields = ('reclamation', 'type', 'commentaire')
        widgets = {
            'reclamation': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
        }

    def __init__(self, numero_commande, *args, **kwargs):
        super(ReclamationForm, self).__init__(*args, **kwargs)
        self.fields['reclamation'].queryset = ReclamationsHandler.objects.get(commande_numero_commande=numero_commande)


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ('libelle', 'description')
        widgets = {
            'libelle': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'description': forms.Textarea(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),

             }

class TrancheForm(forms.ModelForm):
    class Meta:
        model = Tranche
        fields = ('min_weight', 'max_weight', 'price', 'commission','package')
        widgets = {
            'min_weight': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'max_weight': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'commission': forms.NumberInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'package': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),

             }