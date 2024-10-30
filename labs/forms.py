from django import forms
from . import models


class LabAddForm(forms.ModelForm):
    class Meta:
        model = models.Laboratory
        fields = [
            'name',
            'short_name',
            'location',
            'country',
            'latitude',
            'longitude',
            'leadership_area',
            'contact_email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter laboratory name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
            'leadership_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leadership area'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact email'}),
        }
