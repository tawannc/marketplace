from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, ReviewVendedor
from products.models import Product
from django.http import HttpResponse
from orders.models import OrderItem, Order
from django.contrib.auth.decorators import login_required

def criar_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Regra: só avalia quem comprou e recebeu
    comprou = OrderItem.objects.filter(
        order__user=request.user,
        order__status='ENTREGUE',
        product=product
    ).exists()

    if not comprou:
        return HttpResponse("Você só pode avaliar produtos que comprou.")

    if request.method == 'POST':
        Review.objects.create(
            product=product,
            user=request.user,
            rating=request.POST['rating'],
            comment=request.POST.get('comment', '')
        )
        return redirect('produto_publico', product_id)

    return render(request, 'reviews/criar_review.html', {'product': product})

@login_required
def avaliar_pedido(request, order_id):
    # Garantir que o pedido existe e pertence ao comprador logado
    order = get_object_or_404(Order, id=order_id, buyer=request.user.buyerprofile)

    # Só pode avaliar pedido entregue
    if order.status != "delivered":
        return HttpResponse("Você só pode avaliar pedidos entregues.")

    # Impedir avaliação duplicada
    if ReviewVendedor.objects.filter(order=order).exists():
        return HttpResponse("Este pedido já foi avaliado.")

    if request.method == "POST":
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        ReviewVendedor.objects.create(
            order=order,
            buyer=order.buyer,
            seller=order.seller,
            rating=rating,
            comment=comment
        )

        return redirect("minhas_compras")

    return render(request, "reviews/avaliar_pedido.html", {
        "order": order
    })