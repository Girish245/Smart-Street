from cmath import log
from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm


def userLogin(request):
    
    if request.user.is_authenticated:  # this will redirect the user to index page if the user is already logged in and trying to access the login form again
        return redirect('index')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = Account.objects.get(email=email)
        except:
            messages.info(request, "User with this email doesn't exist")
            print("User with this email doesn't exist")
            return redirect('login')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "User logged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid login credentials")
            print('Invalid login credentials')

    return render(request, 'accounts/login.html')


def userLogout(request):
    logout(request)
    messages.info(request, "User logged out successfully")
    return redirect('login')


def userRegister(request):
    form = UserRegisterForm()
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "User registered successfully and logged into account!")
            return redirect('index')

    context = {'form': form}
    return render(request, 'accounts/user-register.html', context)