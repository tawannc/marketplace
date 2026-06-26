from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import BuyerRegisterForm, SellerRegisterForm, LoginForm
from .models import BuyerProfile, SellerProfile

def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            buyer = form.save(commit=False)
            buyer.user = user
            buyer.save()
            return redirect('login')
    else:
        form = BuyerRegisterForm()
    return render(request, 'accounts/register_buyer.html', {'form': form})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            seller = form.save(commit=False)
            seller.user = user
            seller.save()
            return redirect('login')
    else:
        form = SellerRegisterForm()
    return render(request, 'accounts/register_seller.html', {'form': form})

def login_view(request):
    erro = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                erro = "Usuário ou senha incorretos"
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'erro': erro})

def logout_view(request):
    logout(request)
    return redirect('home')
