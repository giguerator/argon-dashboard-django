import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Account, Institution

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['parent_institution','number', 'description', 'type', 'current_value']
        widgets = {
            'parent_institution': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={"class": 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'parent_institution': 'Associated Institution Profile',
            'number': 'Account Number',
            'balance': 'Current Balance'
        }

    def clean_number(self):
        number = self.cleaned_data['number']
        if re.search("[0-9]",number) is None:
            raise ValidationError('At least one number required in account number!')
        return number
    
class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'description']

        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={"class": 'form-control'}),
        }
        labels = {
            'name': 'Institution'
        }

    def clean_description(self):
        description = self.cleaned_data['description']
        if re.search(".+",description) is None:
            raise ValidationError('Description field cannot be empty!')
        return description
        