from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog') + f'?category={self.slug}'

class Product(models.Model):
    COUNTRY_CHOICES = [
        ('RU', 'Россия'),
        ('CN', 'Китай'),
        ('DE', 'Германия'),
        ('FI', 'Финляндия'),
        ('JP', 'Япония'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/%Y/%m/%d/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    characteristics = models.TextField(verbose_name='Характеристики')
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, verbose_name='Страна-производитель')
    production_year = models.IntegerField(verbose_name='Год выпуска')
    model = models.CharField(max_length=100, verbose_name='Модель')
    available = models.BooleanField(default=True, verbose_name='В наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})