from django import forms
from .models import TypeVehicules, Vehicules
from django.utils.translation import ugettext_lazy as _
from utilisateurs.models import User

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
    def __init__(self, *args, **kwargs):
        super(VehiculesForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(agent__is_driver=True)