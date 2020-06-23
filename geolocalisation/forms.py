from .models import City, District
from django import forms

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name', 'country')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '', 'name': '', 'id':'', 'class': 'form-control'}),
            'country': forms.Select(attrs={'placeholder': '', 'name': '', 'id': '', 'class': 'form-control'}),
        }

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ('name', 'city')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '', 'name': '', 'id':'', 'class': 'form-control'}),
            'city': forms.Select(attrs={'placeholder': '', 'name': '', 'id': '', 'class': 'form-control'}),
        }