from django.shortcuts import render

from products.models import Product

def home(request):
    return render(request, 'core/home.html')

def lojas(request):
    return render(request, 'core/lojas.html')
