from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order NO. {order.id}'

    message = f'Dear {order.first_name.title()}, \n\nYou have successfully placed an order.' \
              f'Your order ID is {order.id}'

    mail_sent = send_mail(subject, message, 'ishaqmuhammed191@gmail.com', [order.email])

    return mail_sent
