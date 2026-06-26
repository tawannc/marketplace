from django.urls import path
from .views import adicionar_carrinho, atualizar_carrinho, atualizar_carrinho, category_create, category_delete, category_edit, category_list, product_list, product_create, product_edit, product_delete, remover_carrinho, remover_carrinho, ver_carrinho, ver_carrinho

urlpatterns = [
    path('', product_list, name='product_list'),
    path('novo/', product_create, name='product_create'),
    path('<int:product_id>/editar/', product_edit, name='product_edit'),
    path('<int:product_id>/excluir/', product_delete, name='product_delete'),
    path('categorias/', category_list, name='category_list'),
    path('categorias/nova/', category_create, name='category_create'),
    path('categorias/<int:category_id>/editar/', category_edit, name='category_edit'),
    path('categorias/<int:category_id>/excluir/', category_delete, name='category_delete'),
    path('carrinho/', ver_carrinho, name='ver_carrinho'),
    path('carrinho/add/<int:product_id>/', adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remove/<int:product_id>/', remover_carrinho, name='remover_carrinho'),
    path('carrinho/update/<int:product_id>/', atualizar_carrinho, name='atualizar_carrinho'),

]
