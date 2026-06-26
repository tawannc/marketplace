from django.shortcuts import render, redirect, get_object_or_404
from products.cart import Cart
from .models import Order, OrderItem, ChatMessage
from .pix import gerar_pix
from django.contrib.auth.decorators import login_required
from .utils import calcular_frete
from django.http import HttpResponse

def checkout(request):
    cart = Cart(request)

    if request.method == "POST":
        # Pega o seller do primeiro item
        first_item = next(iter(cart), None)
        seller = first_item['product'].seller if first_item else None

        order = Order.objects.create(
            buyer=request.user.buyerprofile,
            seller=seller,
            total=cart.total(),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price
            )

        pix_code = gerar_pix(order.total, order.id)
        order.pix_code = pix_code
        order.save()

        request.session['cart'] = {}

        return redirect(f"/pedido/{order.id}/")

    return render(request, "orders/checkout.html", {"cart": cart})


def pedido(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "orders/pedido.html", {"order": order})


@login_required
def meus_pedidos(request):
    pedidos = Order.objects.filter(
        buyer=request.user.buyerprofile
    ).order_by('-created_at')

    return render(request, 'orders/meus_pedidos.html', {'pedidos': pedidos})


@login_required
def detalhes_pedido(request, order_id):
    pedido = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user.buyerprofile
    )
    return render(request, 'orders/detalhes_pedido.html', {'pedido': pedido})


@login_required
def calcular_frete_view(request):
    cep_origem = request.user.sellerprofile.cep
    cep_destino = request.user.buyerprofile.cep

    opcoes = calcular_frete(cep_origem, cep_destino)

    return render(request, "orders/frete.html", {
        "opcoes": opcoes,
        "cep_origem": cep_origem,
        "cep_destino": cep_destino
    })


def salvar_frete_pedido(request):
    if request.method == "POST":
        frete = request.POST["frete"]
        codigo, valor = frete.split("|")

        order = Order.objects.filter(
            buyer=request.user.buyerprofile,
            status="AGUARDANDO_FRETE"
        ).first()

        order.shipping_type = "PAC" if codigo == "04510" else "SEDEX"
        order.shipping_price = valor.replace(",", ".")
        order.status = "AGUARDANDO_PAGAMENTO"
        order.save()

        return redirect("checkout")


@login_required
def enviar_comprovante(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        buyer=request.user.buyerprofile
    )

    if request.method == "POST":
        arquivo = request.FILES.get("comprovante")

        if arquivo:
            order.pix_proof = arquivo
            order.status = "paid"
            order.save()
            return redirect("minhas_compras")

    return render(request, "orders/enviar_comprovante.html", {"order": order})


@login_required
def minhas_compras(request):
    buyer = request.user.buyerprofile

    pedidos = Order.objects.filter(
        buyer=buyer
    ).order_by("-created_at")

    return render(request, "orders/minhas_compras.html", {
        "pedidos": pedidos
    })


@login_required
def pedidos_recebidos(request):
    seller = request.user.sellerprofile

    pedidos = Order.objects.filter(
        seller=seller
    ).order_by("-created_at")

    return render(request, "orders/pedidos_recebidos.html", {
        "pedidos": pedidos
    })


@login_required
def gerenciar_pedido(request, order_id):
    seller = request.user.sellerprofile
    order = get_object_or_404(Order, id=order_id, seller=seller)

    if request.method == "POST":
        novo_status = request.POST.get("status")
        rastreio = request.POST.get("tracking_code")

        order.status = novo_status
        order.tracking_code = rastreio
        order.save()

        return redirect("pedidos_recebidos")

    return render(request, "orders/gerenciar_pedido.html", {
        "order": order
    })


@login_required
def chat_pedido(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.buyer.user and request.user != order.seller.user:
        return HttpResponse("Acesso negado")

    if request.method == "POST":
        texto = request.POST.get("mensagem")
        if texto:
            ChatMessage.objects.create(
                order=order,
                sender=request.user,
                text=texto
            )
        return redirect("chat_pedido", order_id=order_id)

    mensagens = order.messages.all().order_by("created_at")

    return render(request, "orders/chat.html", {
        "order": order,
        "mensagens": mensagens
    })
