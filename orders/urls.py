from django.urls import path
from .views import order_create, PaymentSuccess, admin_order_detail, admin_order_pdf

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('pay-success/<str:order_ref>', PaymentSuccess.as_view(), name='paysuccess'),
    path('admin/order/<order_id>', admin_order_detail, name='admin_order_detail'),
    path('order/<order_id>/pdf/', admin_order_pdf, name='admin_order_pdf')

]
