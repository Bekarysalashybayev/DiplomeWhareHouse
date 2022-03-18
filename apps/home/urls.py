# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='index'),
    path('warehouses/', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('clients/', views.client_list, name='clients'),
    path('products/add/', views.product_add, name='product-add'),
    path('products/<int:pk>', views.product_detail, name='product-detail'),
    # path('*', views.notFound, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
