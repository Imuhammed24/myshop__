from django.shortcuts import render, get_object_or_404
from cart.cart import Cart
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/products/list.html', {'category': category,
                                                       'categories': categories,
                                                       'products': products,
                                                       'html_title': 'MYSHOP_HOME'})


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
                  'shop/products/detail.html',
                  {'product': product,
                   'html_title': product.name,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})
