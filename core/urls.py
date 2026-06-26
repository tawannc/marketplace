"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view
from orders.views import chat_pedido, checkout, detalhes_pedido, enviar_comprovante, gerenciar_pedido, meus_pedidos, minhas_compras, pedido, pedidos_recebidos
from products.views import loja_publica, produto_publico, buscar
from reviews.views import avaliar_pedido
from .views import home, lojas
from orders.views import calcular_frete_view
from orders.views import salvar_frete_pedido
from stores.views import seller_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('lojas/', lojas, name='lojas'),
    path('contas/', include('accounts.urls')),
    path('produtos/', include('products.urls')),
    path('loja/<int:seller_id>/', loja_publica, name='loja_publica'),
    path('produto/<int:product_id>/', produto_publico, name='produto_publico'),
    path('buscar/', buscar, name='buscar'),
    path('checkout/', checkout, name='checkout'),
    path('pedido/<int:order_id>/', pedido, name='pedido'),
    path('meus-pedidos/', meus_pedidos, name='meus_pedidos'),
    path('pedido/<int:order_id>/', detalhes_pedido, name='detalhes_pedido'),
    path('contas/login/', login_view, name='login'),
    path('reviews/', include('reviews.urls')),
    path("frete/", calcular_frete_view, name="calcular_frete"),
    path("finalizar-frete/", salvar_frete_pedido, name="salvar_frete"),
    path("pedido/<int:order_id>/comprovante/", enviar_comprovante, name="enviar_comprovante"),
    path("minhas-compras/", minhas_compras, name="minhas_compras"),
    path("pedidos-recebidos/", pedidos_recebidos, name="pedidos_recebidos"),
    path("pedido/<int:order_id>/gerenciar/", gerenciar_pedido, name="gerenciar_pedido"),
    path("pedido/<int:order_id>/chat/", chat_pedido, name="chat_pedido"),
    path("pedido/<int:order_id>/avaliar/", avaliar_pedido, name="avaliar_pedido"),
    path("vendedor/<int:seller_id>/", seller_profile, name="seller_profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)