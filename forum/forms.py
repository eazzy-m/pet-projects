from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Topic


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Е-mail', widget=forms.EmailInput())
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'author', 'topic']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {
            'title': forms.TextInput()
        }