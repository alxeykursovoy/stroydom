from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['login'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['name'],
                last_name=form.cleaned_data['surname']
            )
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'authapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'authapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')