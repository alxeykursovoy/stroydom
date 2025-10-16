from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# ... существующий код ...

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created']
    list_filter = ['status', 'created']
    inlines = [OrderItemInline]
    readonly_fields = ['created', 'updated']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']