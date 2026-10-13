
from django import forms
from .models import Category, Product, Banner


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'image',
            'is_active',
        ]


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = [
            'title',
            'content',
            'image',
            'button_text',
            'button_link',
            'is_active',
        ]
