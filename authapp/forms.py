from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'})
    )
    surname = forms.CharField(
        max_length=50,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'})
    )
    patronymic = forms.CharField(
        max_length=50,
        required=False,
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество'})
    )
    login = forms.CharField(
        max_length=30,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        min_length=6,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password_repeat = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )
    rules = forms.BooleanField(
        label='Я согласен с правилами регистрации',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', name):
            raise ValidationError('Имя может содержать только кириллицу, пробелы и тире')
        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', surname):
            raise ValidationError('Фамилия может содержать только кириллицу, пробелы и тире')
        return surname

    def clean_patronymic(self):
        patronymic = self.cleaned_data['patronymic']
        if patronymic and not re.match(r'^[а-яА-ЯёЁ\s-]*$', patronymic):
            raise ValidationError('Отчество может содержать только кириллицу, пробелы и тире')
        return patronymic

    def clean_login(self):
        login = self.cleaned_data['login']
        if not re.match(r'^[a-zA-Z0-9-]+$', login):
            raise ValidationError('Логин может содержать только латиницу, цифры и тире')
        if User.objects.filter(username=login).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return login

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        
        if password and password_repeat and password != password_repeat:
            raise ValidationError({'password_repeat': 'Пароли не совпадают'})
        
        return cleaned_data

class LoginForm(forms.Form):
    login = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )