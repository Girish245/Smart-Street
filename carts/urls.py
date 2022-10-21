from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-to-cart/<str:pk>/', views.add_to_cart, name='add-to-cart'),
    path('remove-cart-item/<str:pk>/', views.remove_cart_item, name='remove-cart-item'),
    path('remove-cart/<str:pk>/', views.removeCart, name='remove-cart'),
]