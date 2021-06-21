from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from easy_select2 import *


class FirerForm(ModelForm):
    class Meta:
        model = Firer
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.TextInput(attrs={'class': 'form-control'}),
            'coy': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'})
        }


class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = '__all__'
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'target_1': apply_select2(forms.Select),
        }


class FireForm(forms.ModelForm):
    class Meta:
        model = Fire
        fields = ['detail', 'new_target']
        widgets = {
            'detail': apply_select2(forms.Select),
        }
