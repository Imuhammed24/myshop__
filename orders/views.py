import weasyprint
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.views.generic import TemplateView
from paystack.views import payment_state


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
            order.save()
            total_price = cart.get_total_price()
            total_no_item = cart.__len__()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         quantity=item['quantity'],
                                         price=item['price'])
            cart.clear()
            # order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order,
                                                                 'total_price': total_price,
                                                                 'total_no_item': total_no_item,
                                                                 'html_title': 'ORDER MADE'})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form,
                                                        'html_title': 'CHECK_OUT'})


class PaymentSuccess(TemplateView):
    """Land here on successful payment verification."""
    template_name = 'paystack/success-page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        order_id = kwargs['order_ref']

        queryset = Order.objects.get(id=kwargs['order_ref'])

        state = [{'event': payment_state.p_event}, payment_state.p_payment_date,
                 payment_state.p_reference, payment_state.p_email, payment_state.p_json_body]

        context['paystate'] = state
        context['order'] = queryset
        context['tracking_id'] = order_id
        context['html_title'] = 'PURCHASE SUCCESSFUL'
        return context


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='order_{}.pdf'".format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
