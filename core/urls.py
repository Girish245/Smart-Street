from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('store/<slug:category_slug>/', views.store, name='product_by_category'),
    path('search/', views.searchProduct, name='search'),
    path('product-details/<str:pk>/', views.productDetails, name='product-details'),
]