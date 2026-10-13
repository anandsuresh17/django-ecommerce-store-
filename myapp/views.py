
from django.shortcuts import render,get_object_or_404
from .models import Product, Category, Banner
from django.db import models


def home(request):
    banners = Banner.objects.filter(is_active=True).order_by('-created_at')

    products = Product.objects.filter(
        is_active=True
    ).select_related('category').order_by('-created_at')[:3]

    categories = Category.objects.filter(is_active=True).order_by('name')

    context = {
        'banners': banners,
        'products': products,
        'categories': categories,
    }

    return render(request, 'home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    return render(request, 'product_detail.html', {
        'product': product
    })


def category_detail(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('category')

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products
    })



def store(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related('category').order_by('-created_at')

    categories = Category.objects.filter(is_active=True).order_by('name')

    # Search by product name or description
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )

    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    # Filter by price
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            min_price = ''

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            max_price = ''

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'store.html', context)


