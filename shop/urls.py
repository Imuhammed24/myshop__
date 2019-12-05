from django.urls import path

from .views import product_list, product_detail

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<product_id>/<str:slug>/', product_detail, name='product_detail'),
    path('<category_slug>/', product_list, name='product_list_by_category'),
]
