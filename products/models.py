from django.db import models
from django.contrib.auth.models import User
from django.db import models
from accounts.models import SellerProfile

class Category(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def available(self):
        return self.stock > 0 and self.is_active

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products/')

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='variations')
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    dimensions = models.CharField(max_length=100, blank=True)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    name = models.CharField(max_length=50)   # Ex: Cor, Tamanho
    value = models.CharField(max_length=50)  # Ex: Azul, M, 42

    def __str__(self):
        return f"{self.product.name} - {self.color} {self.size} {self.name}: {self.value}"
