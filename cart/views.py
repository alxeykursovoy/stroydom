from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from .models import Order, OrderItem
from products.models import Product
from .forms import OrderForm

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, available=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'Товар "{product.name}" добавлен в корзину!')
        return redirect('product_detail', slug=product.slug)
    
    return redirect('catalog')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif action == 'remove':
            cart_item.delete()
            return JsonResponse({'success': True, 'removed': True})
        
        cart_item.save()
        
        cart = cart_item.cart
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'item_total': cart_item.total_price(),
            'cart_total': cart.total_price(),
            'cart_quantity': cart.total_quantity()
        })
    
    return JsonResponse({'success': False})

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.items.count() == 0:
        messages.error(request, 'Ваша корзина пуста!')
        return redirect('cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = authenticate(username=request.user.username, password=password)
            
            if user is not None:
                # Создаем заказ
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.total_price()
                )
                
                # Создаем элементы заказа
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                # Очищаем корзину
                cart.items.all().delete()
                
                messages.success(request, f'Заказ #{order.id} успешно оформлен! С вами свяжутся для уточнения деталей.')
                return redirect('profile')
            else:
                messages.error(request, 'Неверный пароль! Пожалуйста, попробуйте снова.')
    else:
        form = OrderForm()
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'cart/checkout.html', context)