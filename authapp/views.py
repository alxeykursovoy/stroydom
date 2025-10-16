from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re

def register_view(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()
        username = request.POST.get('login', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_repeat = request.POST.get('password_repeat', '')
        rules = request.POST.get('rules')
        
        # Валидация
        errors = []
        
        # Проверка обязательных полей
        if not name:
            errors.append('Имя обязательно для заполнения')
        if not surname:
            errors.append('Фамилия обязательна для заполнения')
        if not username:
            errors.append('Логин обязателен для заполнения')
        if not email:
            errors.append('Email обязателен для заполнения')
        if not password:
            errors.append('Пароль обязателен для заполнения')
        if not password_repeat:
            errors.append('Повтор пароля обязателен')
        if not rules:
            errors.append('Необходимо согласие с правилами регистрации')
        
        # Валидация форматов
        if name and not re.match(r'^[а-яА-ЯёЁ\s-]+$', name):
            errors.append('Имя может содержать только кириллицу, пробелы и тире')
        
        if surname and not re.match(r'^[а-яА-ЯёЁ\s-]+$', surname):
            errors.append('Фамилия может содержать только кириллицу, пробелы и тире')
        
        if patronymic and not re.match(r'^[а-яА-ЯёЁ\s-]*$', patronymic):
            errors.append('Отчество может содержать только кириллицу, пробелы и тире')
        
        if username and not re.match(r'^[a-zA-Z0-9-]+$', username):
            errors.append('Логин может содержать только латиницу, цифры и тире')
        
        # Проверка уникальности
        if username and User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким логином уже существует')
        
        if email and User.objects.filter(email=email).exists():
            errors.append('Пользователь с таким email уже существует')
        
        # Проверка пароля
        if password and len(password) < 6:
            errors.append('Пароль должен содержать минимум 6 символов')
        
        if password and password_repeat and password != password_repeat:
            errors.append('Пароли не совпадают')
        
        # Если есть ошибки - показываем их
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Создаем пользователя
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=name,
                    last_name=surname
                )
                messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
                return redirect('/auth/login/')
            except Exception as e:
                messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
    
    return render(request, 'authapp/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login', '').strip()
        password = request.POST.get('password', '')
        
        if not username:
            messages.error(request, 'Введите логин')
        elif not password:
            messages.error(request, 'Введите пароль')
        else:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                return redirect('/')
            else:
                messages.error(request, 'Неверный логин или пароль')
    
    return render(request, 'authapp/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('/')