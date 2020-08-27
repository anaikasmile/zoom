#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Agences
from utilisateurs.models import User
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

