from django import forms

class OrderForm(forms.Form):
    password = forms.CharField(
        label='Пароль для подтверждения',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль для подтверждения заказа'
        })
    )