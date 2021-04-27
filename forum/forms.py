from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Topic
import re


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
                   'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
                   }


class CommForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'topic']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
