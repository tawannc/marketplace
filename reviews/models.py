from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import BuyerProfile
from orders.models import Order
from accounts.models import BuyerProfile, SellerProfile

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 a 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'buyer')

    def __str__(self):
        return f"{self.product.name} - {self.rating} estrelas"

class ReviewVendedor(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)

    rating = models.IntegerField()  # 1 a 5
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação {self.rating} estrelas - Pedido {self.order.id}"