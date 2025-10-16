from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order

@staff_member_required
def order_management(request):
    status_filter = request.GET.get('status', 'all')
    
    if status_filter == 'all':
        orders = Order.objects.all().prefetch_related('items', 'user')
    else:
        orders = Order.objects.filter(status=status_filter).prefetch_related('items', 'user')
    
    status_counts = {
        'new': Order.objects.filter(status='new').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
        'all': Order.objects.count()
    }
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_counts': status_counts,
    }
    return render(request, 'admin/order_management.html', context)

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        cancel_reason = request.POST.get('cancel_reason', '')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            if new_status == 'cancelled':
                order.cancel_reason = cancel_reason
            order.save()
            
            messages.success(request, f'Статус заказа #{order_id} обновлен на "{order.get_status_display()}"')
        else:
            messages.error(request, 'Неверный статус заказа')
    
    return redirect('order_management')