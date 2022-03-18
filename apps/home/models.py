# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Block(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    color = models.CharField(max_length=10, null=True, )

    class Meta:
        verbose_name = "Блок"
        verbose_name_plural = "Блок"

    def __str__(self):
        return f"{self.name}"


class Row(TimeStampedModel):
    number = models.IntegerField()
    block = models.ForeignKey('home.Block',
                              related_name='rows',
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)

    class Meta:
        verbose_name = "Ряд"
        verbose_name_plural = "Ряд"

    def __str__(self):
        return f"{self.number}"


class Column(TimeStampedModel):
    number = models.IntegerField()
    is_free = models.BooleanField(default=True)
    capacity = models.IntegerField(default=300)
    free_capacity = models.IntegerField(default=300)
    row = models.ForeignKey('home.Row',
                            related_name='columns',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True)

    class Meta:
        verbose_name = "Столбец"
        verbose_name_plural = "Столбец"
        unique_together = ['number', 'row']

    def __str__(self):
        return f"{self.number}"


class Category(TimeStampedModel):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"


class Client(TimeStampedModel):
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.first_name}"


class Product(TimeStampedModel):
    code = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    capacity = models.IntegerField(default=0)
    weight = models.FloatField(default=0.00)
    price = models.FloatField(default=0)
    client = models.ForeignKey('home.Client',
                               related_name='products',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    user = models.ForeignKey('auth.User',
                             related_name='products',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True
                             )
    category = models.ForeignKey('home.Category',
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"


class ColumnProduct(TimeStampedModel):
    product = models.ForeignKey('home.Product',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    column = models.ForeignKey('home.Column',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)
    capacity = models.IntegerField(default=0)


class ClientCode(TimeStampedModel):
    product = models.ForeignKey('home.Product',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    code = models.IntegerField(default=0)
