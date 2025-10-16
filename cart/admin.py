from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated', 'total_quantity', 'total_price']
    readonly_fields = ['created', 'updated']

    def total_quantity(self, obj):
        return obj.total_quantity()
    total_quantity.short_description = 'Кол-во товаров'

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Общая сумма'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    list_filter = ['cart__user']

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Общая стоимость'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_info', 'total_price', 'total_quantity', 'status', 'created', 'updated']
    list_filter = ['status', 'created', 'updated']
    list_editable = ['status']
    inlines = [OrderItemInline]
    readonly_fields = ['created', 'updated', 'user', 'total_price']
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'total_price', 'created', 'updated')
        }),
        ('Статус заказа', {
            'fields': ('status', 'cancel_reason')
        }),
    )
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'cancel_with_reason']

    def user_info(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name} ({obj.user.email})"
    user_info.short_description = 'Пользователь'

    def total_quantity(self, obj):
        return obj.total_quantity()
    total_quantity.short_description = 'Кол-во товаров'

    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
        self.message_user(request, f"{queryset.count()} заказ(ов) переведено в статус 'В обработке'")
    mark_as_processing.short_description = "✅ Подтвердить заказы"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
        self.message_user(request, f"{queryset.count()} заказ(ов) переведено в статус 'Отправлен'")
    mark_as_shipped.short_description = "🚚 Отметить как отправленные"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f"{queryset.count()} заказ(ов) переведено в статус 'Доставлен'")
    mark_as_delivered.short_description = "📦 Отметить как доставленные"

    def cancel_with_reason(self, request, queryset):
        if 'apply' in request.POST:
            reason = request.POST.get('reason', '')
            if not reason:
                self.message_user(request, "Необходимо указать причину отказа!", level='ERROR')
                return
            
            queryset.update(status='cancelled', cancel_reason=reason)
            self.message_user(request, f"{queryset.count()} заказ(ов) отменено с причиной: {reason}")
            return
        
        return render(request, 'admin/cancel_reason.html', context={
            'orders': queryset,
            'action': 'cancel_with_reason',
        })
    cancel_with_reason.short_description = "❌ Отменить заказы с указанием причины"

    def response_change(self, request, obj):
        if "_confirm" in request.POST:
            obj.status = 'processing'
            obj.save()
            self.message_user(request, f"Заказ #{obj.id} подтвержден")
            return redirect(".")
        elif "_cancel" in request.POST:
            return redirect(reverse('admin:cart_order_changelist'))
        return super().response_change(request, obj)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']
    list_filter = ['order__status']

    def total_price(self, obj):
        return f"{obj.total_price()} ₽"
    total_price.short_description = 'Общая стоимость'