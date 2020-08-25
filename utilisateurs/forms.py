#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Person, User, Identity

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, PhoneNumberInternationalFallbackWidget
from django.forms.models import inlineformset_factory

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder':_(u'Email'),'name':'','id':'','class':'form-control'}),
            'username': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),

              }


class SignUpForm(forms.Form):
    SEXE = (
        (u'F', _(u'Feminin')),
        (u'M', _(u'Masculin')),
    )
    password1 = forms.PasswordInput(attrs={'required': True,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
    password2 = forms.PasswordInput(attrs={'required': True,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
          
    sexe = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}), choices=SEXE)
    tel = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='+228',attrs={'class': 'form-control'}))
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'customFileLang', 'lang': 'fr'}))
    birth_date = forms.DateField(help_text='Requis. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    job = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control','placeholder': _(u'')}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        user.person.birth_date = self.cleaned_data.get('birth_date')
        user.person.tel = self.cleaned_data.get('tel').as_e164
        user.person.sexe = self.cleaned_data.get('sexe')
        user.person.adresse = self.cleaned_data.get('adresse')
        user.person.save()


class UserRegistrationForm(forms.ModelForm):
    SEXE = (
        (u'F', _(u'Feminin')),
        (u'M', _(u'Masculin')),
    )
    password1 = forms.PasswordInput(attrs={'required': True,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
    password2 = forms.PasswordInput(attrs={'required': True,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
          
    sexe = forms.ChoiceField(required=True, widget=forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}), choices=SEXE)
    tel = PhoneNumberField(required=True, widget=PhoneNumberPrefixWidget(initial='+228',attrs={'class': 'form-control'}))
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'customFileLang', 'lang': 'fr'}))
    birth_date = forms.DateField(help_text='Requis. Format: YYYY-MM-DD', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    job = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control','placeholder': _(u'')}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", }), required=True)

    class Meta:
        model = User
        exclude = ['password','last_login', 'is_staff', 'is_superuser', 'is_active','user_type', 'date_joined']

class UserRegistrationForm1(forms.ModelForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name','email')
        widgets = {
            #'user_type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control',}),
            'email': forms.TextInput(attrs={'required': False,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            
        }

class UserRegistrationForm2(forms.ModelForm):
   
    class Meta:
        model = Person
        fields = ('sexe', 'tel', 'photo', 'birth_date', 'adresse', 'job')
        widgets = {
            #'user_type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'sexe': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'tel': PhoneNumberPrefixWidget(initial='+228',attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'class': 'form-control', 'required': False}),
            'adresse': forms.Textarea(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'job': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'photo': forms.FileInput(attrs={'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input', 'lang': 'fr'}),

        }

# class UserRegistrationForm3(forms.ModelForm):
   
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2')
#         widgets = {
#             #'user_type': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'required': False,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
#             'password2': forms.PasswordInput(attrs={'required': False,'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
#             'username': forms.TextInput(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control','autocomplete':'off'}),

#         }



class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('user','tel', 'sexe', 'adresse', 'birth_date', 'job', 'photo')
        widgets = {
            'sexe': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'tel': PhoneNumberPrefixWidget(initial='+228',attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date', 'class': 'form-control', 'required': False}),
            'adresse': forms.Textarea(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control','rows': 5 }),
            'job': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'photo': forms.FileInput(attrs={'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input', 'lang': 'fr'}),

        }

ProfileInlineFormset = inlineformset_factory(
    User, Person, fields=('tel', 'sexe', 'adresse', 'birth_date', 'job', 'photo'),
    widgets = {
            'sexe': forms.Select(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'tel': PhoneNumberPrefixWidget(initial='+228', attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': '', 'class': 'form-control', 'required': False}),
            'adresse': forms.Textarea(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', 'rows': 5}),
            'job': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'photo': forms.FileInput(attrs={'placeholder': _(u''), 'name': '', 'id': 'customFileLang', 'class': 'custom-file-input', 'lang': 'fr'}),
   
        },can_delete = False, extra=1
    )


class IdentityForm(forms.ModelForm):
    class Meta:
        model = Identity
        fields = ('type', 'reference', 'photo', 'initiated_at', 'expired_at', 'contact_name', 'contact_tel')
        widgets = {
            'type': forms.Select(attrs={'required':True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'required':True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'placeholder': _(u'Photo'), 'name': '', 'id': '', 'class': 'form-control'}),
            'initiated_at': forms.DateInput(format='%d/%m/%Y', attrs={'required': True, 'type': '',  'name': '', 'id': '', 'class': 'form-control'}),
            'expired_at': forms.DateInput(format='%d/%m/%Y', attrs={'required': True, 'type': '', 'name': '', 'id': '', 'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
            'contact_tel': forms.TextInput(
                attrs={'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control'}),
        }

class RegistrationFormStep1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'required': True, 'placeholder': _(u''), 'name': '', 'id': '', 'class': 'form-control',}),
            
    }

# class RegistrationFormStep2(forms.ModelForm):
#     class Meta:
#         model = Registration
#         fields = ['passport', 'hotel_registration']
#         exclude = ('first_name', 'last_name', 'event' , 'city_origin', 'flight_date_from', 'flight_date_to', 'require_transfer')
#         widgets = {
#              'passport': forms.NumberInput(attrs={'placeholder':'Escriba su pasaporte'})
#         }