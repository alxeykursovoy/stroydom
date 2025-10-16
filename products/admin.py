from django.contrib import admin
from .models import Category, Product
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def product_count(self, obj):
        return obj.product_set.count()  # Исправлено с products на product_set
    product_count.short_description = 'Количество товаров'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available_badge', 'production_year', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'country', 'production_year']
    list_editable = ['price', 'production_year']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created', 'updated']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'available')
        }),
        ('Характеристики', {
            'fields': ('characteristics', 'country', 'production_year', 'model')
        }),
        ('Даты', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    actions = ['make_available', 'make_unavailable']

    def available_badge(self, obj):
        if obj.available:
            return format_html(
                '<span style="background-color: green; color: white; padding: 4px 8px; border-radius: 10px;">✓ В наличии</span>'
            )
        else:
            return format_html(
                '<span style="background-color: red; color: white; padding: 4px 8px; border-radius: 10px;">✗ Нет в наличии</span>'
            )
    available_badge.short_description = 'Статус'

    def make_available(self, request, queryset):
        queryset.update(available=True)
    make_available.short_description = "Сделать доступными"

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
    make_unavailable.short_description = "Сделать недоступными"