from django import forms
from django.core.exceptions import ValidationError
import re


class WeatherForm(forms.Form):
    name = forms.CharField(label='Название города', widget=forms.TextInput(attrs={'class': 'form-control'}))
