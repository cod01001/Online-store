from . import views
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    # product_list: шаблон с именем product_list,
    # который вызывает product_list view без каких-либо параметров

    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    # product_list_by_category, который предоставляет параметр category_slug
    # в представлении для фильтрации продуктов по данной категории

    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    # product_list_by_category, который предоставляет параметр category_slug в
    # представлении для фильтрации продуктов по данной категории
            ]
