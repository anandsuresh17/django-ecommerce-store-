from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
     path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'category/<int:category_id>/',
        views.category_detail,
        name='category_detail'
    ),

]