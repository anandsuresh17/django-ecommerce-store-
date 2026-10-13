
from django.shortcuts import render,get_object_or_404
from .models import Product, Category, Banner


def home(request):
    banners = Banner.objects.filter(is_active=True).order_by('-created_at')
    products = Product.objects.filter(is_active=True).select_related(
        'category'
    ).order_by('-created_at')[:8]
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

    return render(request, 'myapp/product.html', {
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

    return render(request, 'myapp/category.html', {
        'category': category,
        'products': products
    })


def store(request):
    products = Product.objects.filter(
        is_active=True
    ).select_related('category').order_by('-created_at')

    categories = Category.objects.filter(
        is_active=True
    ).order_by('name')

    return render(request, 'myapp/store.html', {
        'products': products,
        'categories': categories,
    })

