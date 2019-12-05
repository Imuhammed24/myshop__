from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, CartUpdateProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        # create an 'update_quantity_form' for all objects in d cart, then set their values to initial value
        item['update_quantity_form'] = CartUpdateProductForm(initial={'quantity': item['quantity'],
                                                             'update': True})

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products, max_results=4)

    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/detail.html', {'cart': cart,
                                                'html_title': 'My Shopping Cart',
                                                'coupon_apply_form': coupon_apply_form,
                                                'recommended_products': recommended_products})
