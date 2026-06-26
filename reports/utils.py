from django.db.models import Sum, Count
from orders.models import Order, OrderItem

def top_selling_products(seller):
    return (OrderItem.objects
            .filter(order__seller=seller, order__status__in=['paid', 'shipped', 'delivered'])
            .values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:10])
