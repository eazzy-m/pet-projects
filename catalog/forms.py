from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from catalog.models import Order, MobTel, Television, Feedback


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'comment'
        )


class MobtelForm(forms.ModelForm):
    class Meta:
        model = MobTel
        fields = '__all__'
        widgets = {'product_category': forms.HiddenInput()}

class TelevisionForm(forms.ModelForm):
    class Meta:
        model = Television
        fields = '__all__'
        widgets = {'product_category': forms.HiddenInput()}



class FeedBackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = (
            'title', 'text', 'dignities', 'disadvantages', 'estimation'
        )
        # widgets = {'product_category': forms.HiddenInput()}