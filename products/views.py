from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import SellerProfile
from .models import Product, ProductImage, Category
from .forms import ProductForm, ProductImageForm, CategoryForm
from django.db.models import Q
from .cart import Cart

@login_required
def product_list(request):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    products = Product.objects.filter(seller=seller)
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def product_create(request):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile

    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(seller=seller)

        files = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()

            for f in files[:5]:
                ProductImage.objects.create(product=product, image=f)

            return redirect('product_list')

    else:
        form = ProductForm()
        form.fields['category'].queryset = Category.objects.filter(seller=seller)

    return render(request, 'products/product_create.html', {'form': form})


@login_required
def product_edit(request, product_id):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    product = get_object_or_404(Product, id=product_id, seller=seller)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        form.fields['category'].queryset = Category.objects.filter(seller=seller)

        files = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            for f in files[:5]:
                ProductImage.objects.create(product=product, image=f)

            return redirect('product_list')

    else:
        form = ProductForm(instance=product)
        form.fields['category'].queryset = Category.objects.filter(seller=seller)

    return render(request, 'products/product_edit.html', {'form': form, 'product': product})


@login_required
def product_delete(request, product_id):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    product = get_object_or_404(Product, id=product_id, seller=seller)

    product.is_active = False
    product.save()

    return redirect('product_list')


@login_required
def category_list(request):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    categories = Category.objects.filter(seller=seller)
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.seller = seller
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'products/category_create.html', {'form': form})


@login_required
def category_edit(request, category_id):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    category = get_object_or_404(Category, id=category_id, seller=seller)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/category_edit.html', {'form': form})


@login_required
def category_delete(request, category_id):
    if not hasattr(request.user, "sellerprofile"):
        return redirect("home")

    seller = request.user.sellerprofile
    category = get_object_or_404(Category, id=category_id, seller=seller)
    category.delete()
    return redirect('category_list')


def loja_publica(request, seller_id):
    seller = get_object_or_404(SellerProfile, id=seller_id)

    produtos = Product.objects.filter(seller=seller, is_active=True)
    categorias = Category.objects.filter(seller=seller)

    return render(request, 'products/loja_publica.html', {
        'seller': seller,
        'produtos': produtos,
        'categorias': categorias,
    })


def produto_publico(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    imagens = product.images.all()

    relacionados = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'products/produto_publico.html', {
        'product': product,
        'imagens': imagens,
        'relacionados': relacionados,
    })


def adicionar_carrinho(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect('ver_carrinho')


def remover_carrinho(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('ver_carrinho')


def atualizar_carrinho(request, product_id):
    cart = Cart(request)
    quantidade = int(request.POST.get('quantidade', 1))
    cart.update(product_id, quantidade)
    return redirect('ver_carrinho')


def ver_carrinho(request):
    cart = Cart(request)
    return render(request, 'products/carrinho.html', {'cart': cart})


def buscar(request):
    termo = request.GET.get('q', '')

    produtos = Product.objects.filter(
        Q(name__icontains=termo) |
        Q(description__icontains=termo)
    ).filter(is_active=True)

    categorias = Category.objects.filter(
        name__icontains=termo
    )

    lojas = SellerProfile.objects.filter(
        store_name__icontains=termo
    )

    return render(request, 'products/busca.html', {
        'termo': termo,
        'produtos': produtos,
        'categorias': categorias,
        'lojas': lojas,
    })
