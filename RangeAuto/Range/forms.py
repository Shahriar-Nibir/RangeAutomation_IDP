from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from searchableselect.widgets import SearchableSelect
from django import forms
from .models import *
from ajax_select import make_ajax_field


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
            # 'number': forms.TextInput(attrs={'class': 'form-control'}),
            # 'target_1': forms.ChoiceField(attrs={'class': 'form-control'}),
            # 'target_2': forms.ChoiceField(attrs={'class': 'form-control'})
        }
    # target_1 = make_ajax_field(Detail, 'target_1', 'firer')
    # target_2 = make_ajax_field(Detail, 'target_2', 'firer')
