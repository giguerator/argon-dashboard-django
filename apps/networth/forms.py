import re

from django import forms
from django.core.exceptions import ValidationError

from .models import ManualAsset

class ManualAssetForm(forms.ModelForm):
    class Meta:
        model = ManualAsset
        fields = ['description','category', 'current_value']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),

            'description': forms.TextInput(attrs={"class": 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        labels = {
            'current_value': 'Current Value'
        }