from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def catalog_view(request):
    # Получаем все товары в наличии
    products = Product.objects.filter(available=True)
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Сортировка
    sort = request.GET.get('sort', 'newest')
    if sort == 'name':
        products = products.order_by('name')
    elif sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'year':
        products = products.order_by('-production_year')
    else:  # newest
        products = products.order_by('-created')
    
    # Получаем все категории для фильтра
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'current_sort': sort,
    }
    return render(request, 'products/catalog.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)