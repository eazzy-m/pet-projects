from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from catalog.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'comment'
        )
