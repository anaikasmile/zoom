#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import AgenceUser
from utilisateurs.models import User
from agences.models import Agences

from django.utils.translation import ugettext_lazy as _

class AgenceUserForm(forms.ModelForm):
    class Meta:
        model = AgenceUser
        fields = ('agence', 'agent')
        widgets = {
            'agence': forms.Select(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            #'agent': forms.Select(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'})
             }
    def __init__(self, *args, **kwargs):
        agent = kwargs.pop("agent")
        agence = kwargs.pop("agence")
        super(AgenceUserForm, self).__init__(*args, **kwargs)
        self.fields['agent'] = forms.ModelChoiceField(queryset=User.objects.all(),
                                                             initial=agent,
                                                             widget=forms.Select(attrs={'class': 'form-control'})
                                                             )
        self.fields['agence'] = forms.ModelChoiceField(queryset=Agences.objects.all(),
                                                             initial=agence,
                                                             widget=forms.Select(attrs={'class': 'form-control'})
                                                             )