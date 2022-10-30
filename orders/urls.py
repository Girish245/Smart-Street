from django.urls import path
from . import views


urlpatterns = [
    path('checkout/', views.billing_address, name='checkout'),
    path('place-order/', views.place_order, name='place-order'),
    path('payments/', views.payment, name='payments'),
    path('order-complete/<str:pk>/', views.orderComplete, name='order-complete'),
]