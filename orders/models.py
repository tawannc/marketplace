from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Variation
from accounts.models import BuyerProfile, SellerProfile

ORDER_STATUS_CHOICES = (
    ('pending', 'Aguardando pagamento'),
    ('paid', 'Pago'),
    ('canceled', 'Cancelado'),
    ('shipped', 'Enviado'),
    ('delivered', 'Entregue'),
)

class Order(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    total = models.DecimalField(max_digits=10, decimal_places=2)

    # FRETE (Sprint 8)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_type = models.CharField(max_length=20, blank=True, null=True)

    # PIX (Sprint 9)
    pix_proof = models.FileField(upload_to='pix_proofs/', blank=True, null=True)

    # RASTREIO (Sprint 10)
    tracking_code = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    # Sprint 7 — variações
    variation = models.ForeignKey(Variation, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.unit_price

class ChatMessage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.sender.username} no pedido {self.order.id}"
