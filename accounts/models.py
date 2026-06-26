from django.db import models

from django.db import models
from django.contrib.auth.models import User

import reviews
from reviews.models import ReviewVendedor

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    address = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)

    def __str__(self):
        return f"Comprador: {self.user.username}"

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    address = models.CharField(max_length=255)
    cep = models.CharField(max_length=9)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    pix_key = models.CharField(max_length=200)

    @property
    def rating_average(self):
        from reviews.models import ReviewVendedor
        reviews = ReviewVendedor.objects.filter(seller=self)
        if not reviews.exists():
            return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def __str__(self):
        return f"Loja: {self.store_name}"

    
