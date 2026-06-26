from django import forms
from django.contrib.auth.models import User
from .models import BuyerProfile, SellerProfile

class BuyerRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = BuyerProfile
        fields = ['cpf', 'address', 'cep', 'city', 'state']

class SellerRegisterForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = SellerProfile
        fields = ['store_name', 'description', 'address', 'cep', 'city', 'state', 'pix_key']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
