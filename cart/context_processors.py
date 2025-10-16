from .models import Cart

def cart_context(request):
    context = {}
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        context['cart_count'] = cart.total_quantity()
    else:
        context['cart_count'] = 0
    return context