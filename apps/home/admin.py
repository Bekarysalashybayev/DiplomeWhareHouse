# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from apps.home.models import *


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ["number", "block"]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ["number", "row", "capacity", "free_capacity", "is_free"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "phone"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "capacity", "price",
                    "weight", "client", "category", "is_active"]
    search_fields = ["name", "client"]
    list_filter = ['client', 'category']


@admin.register(ClientCode)
class ClientCodeAdmin(admin.ModelAdmin):
    list_display = ["product", "code"]
    search_fields = ["product"]


@admin.register(ColumnProduct)
class ColumnProductAdmin(admin.ModelAdmin):
    list_display = ["product", "column", 'capacity']
    search_fields = ["product"]
