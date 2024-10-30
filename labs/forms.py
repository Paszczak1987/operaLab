from django import forms
import re
from . import models


class LabAddForm(forms.ModelForm):
    class Meta:
        model = models.Laboratory
        fields = [
            'name', 'short_name', 'lab_code', 'description',
            'street', 'number', 'zip_code', 'city', 'country',
            'latitude', 'longitude', 'leadership_area', 'contact_email'
        ]
        labels = {
            'name': 'Laboratory full name',
            'short_name': 'Shortend name',
            'contact_email': 'Email address'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter laboratory name'}),
            'short_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter short name'}),
            'lab_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Set lab code'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Laboratory description'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street name'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude'}),
            'leadership_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leadership area'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }
    
    def clean_short_name(self):
        short_name = self.cleaned_data.get('short_name')
        if not isinstance(short_name, str) or not short_name.strip():
            raise forms.ValidationError("Short name must be a valid string.")
        return short_name
    
    def clean_leadership_area(self):
        leadership_area = self.cleaned_data.get('leadership_area')
        if re.search(r'\d', leadership_area):
            raise forms.ValidationError("Leadership area cannot contain numeric values.")
        return leadership_area
    
    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude is not None and latitude < 0:
            raise forms.ValidationError("Latitude must be a non-negative value.")
        return latitude
    
    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude is not None and longitude < 0:
            raise forms.ValidationError("Longitude must be a non-negative value.")
        return longitude
