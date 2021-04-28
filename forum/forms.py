from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Topic
from captcha.fields import CaptchaField, CaptchaTextInput


class CustomCaptcha(CaptchaTextInput):
    template_name = 'forum/custom_field.html'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Ваш логин...'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Ваш пароль...'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Ваш логин...'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Ваш пароль...'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Повторите пароль...'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Ваш E-mail...'}))
    captcha = CaptchaField(label='Капча', widget=CustomCaptcha(attrs={'class': 'form-control',
                                                                      'placeholder': 'Введите капчу'}))

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
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'placeholder': 'Не более 250 символов...',
                                          'rows': 5})
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Не более 50 символов...'})
        }
