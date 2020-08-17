#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import AgenceUser

from django.utils.translation import ugettext_lazy as _

class AgenceUserForm(forms.ModelForm):
    class Meta:
        model = AgenceUser
        fields = ('agence', 'agent')
        widgets = {
            'agence': forms.Select(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'}),
            'agent': forms.Select(attrs={'placeholder':_(u''),'name':'','id':'','class':'form-control'})
             }
    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)