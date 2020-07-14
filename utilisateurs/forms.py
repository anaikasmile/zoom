#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Person, User, Identity

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder':_(u'Email'),'name':'','id':'','class':'form-control'}),
              }


class UserRegistrationForm(UserCreationForm):
    SEXE = (
        (u'F', _(u'Feminin')),
        (u'M', _(u'Masculin')),
    )
    sexe = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}), choices=SEXE)
    tel = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'customFileLang', 'lang': 'en'}))
    birth_date = forms.DateField(help_text='Requis. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    adresse = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    job = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'password1', 'password2', 'email')
        widgets = {
            #'user_type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control',}),
            'email': forms.TextInput(attrs={'required': True,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),

        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('tel', 'sexe', 'adresse', 'birth_date', 'job', 'photo')
        widgets = {
            'sexe': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': False}),
            'adresse': forms.Textarea(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'job': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'photo': forms.FileInput(attrs={'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input', }),

        }

class IdentityForm(forms.ModelForm):
    class Meta:
        model = Identity
        fields = ('type', 'reference', 'photo', 'initiated_at', 'expired_at', 'contact_name', 'contact_tel')
        widgets = {
            'type': forms.Select(attrs={'required':True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'required':True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'placeholder': _(u'Photo'), 'name': '', 'id': '', 'class': 'form-control'}),
            'initiated_at': forms.DateInput(format='%d/%m/%Y', attrs={'required': True, 'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'expired_at': forms.DateInput(format='%d/%m/%Y', attrs={'required': True, 'type': 'date', 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'contact_tel': forms.TextInput(
                attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
        }