from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('user-register/', views.userRegister, name='user-register'),
    path('profile/', views.profile, name='profile'),
]