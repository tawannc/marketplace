from django.urls import path
from .views import register_buyer, register_seller, login_view, logout_view

urlpatterns = [
    path('registrar/comprador/', register_buyer, name='register_buyer'),
    path('registrar/vendedor/', register_seller, name='register_seller'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
