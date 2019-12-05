import os
from celery import Celery
from django.conf import settings


# set default django settings module for the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')


app = Celery('myshop')
app.config_from_object('django.conf:settings')

# tells celery to execute asynchronous tasks in the application; 'myshop.product'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
