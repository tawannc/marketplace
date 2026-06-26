from django.urls import path
from . import views

urlpatterns = [
    # Produtos
    path('', views.product_list, name='product_list'),
    path('novo/', views.product_create, name='product_create'),
    path('<int:product_id>/editar/', views.product_edit, name='product_edit'),
    path('<int:product_id>/excluir/', views.product_delete, name='product_delete'),

    # Categorias
    path('categorias/', views.category_list, name='category_list'),
    path('categorias/nova/', views.category_create, name='category_create'),
    path('categorias/<int:category_id>/editar/', views.category_edit, name='category_edit'),
    path('categorias/<int:category_id>/excluir/', views.category_delete, name='category_delete'),

    # Carrinho
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:product_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remove/<int:product_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/update/<int:product_id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
]
