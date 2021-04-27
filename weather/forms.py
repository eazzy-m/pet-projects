from django import forms


class WeatherForm(forms.Form):
    name = forms.CharField(max_length=32, label='Город')