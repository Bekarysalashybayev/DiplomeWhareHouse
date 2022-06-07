# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import random
import string

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse

from apps.home.models import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    bloc_list = Block.objects.all()

    # for bl in bloc_list:
    #     for i in range(1, 10):
    #         row = Row.objects.create(number=i, block=bl)
    #         row.save()
    # bloc_list = Row.objects.all()
    #
    # for bl in bloc_list:
    #     for i in range(1, 21):
    #         row = Column.objects.create(number=i, is_free=True, capacity=20000, free_capacity=20000, row=bl)
    #         row.save()

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def home(request):
    context = {'segment': 'main'}

    block_list = Block.objects.prefetch_related('rows').prefetch_related('rows__columns')

    context['list'] = block_list

    html_template = loader.get_template('home/home.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def product_list(request):
    context = {'segment': 'product'}

    list = Product.objects.select_related('client').all()
    context['list'] = list

    html_template = loader.get_template('home/products/product-list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def client_list(request):
    context = {'segment': 'client'}

    list = Client.objects.all()
    context['list'] = list

    html_template = loader.get_template('home/clients/client-list.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def product_detail(request, pk):
    context = {'segment': 'product'}

    product = Product.objects.filter(id=pk, is_active=True).select_related('client')
    product = product.first()
    if product:
        context['list'] = product

        col_list = ColumnProduct.objects.filter(product=product).select_related('column') \
            .prefetch_related('column__row').prefetch_related('column__row__block')

        if request.method == "POST":
            code = ClientCode.objects.filter(product=product)
            print(code.first().code)
            print(request.POST['code'])

            if str(code.first().code) == str(request.POST['code']):
                for col in col_list:
                    column = Column.objects.get(id=col.column.id)
                    column.free_capacity += col.capacity
                    column.is_free = True
                    column.save()
                    col.delete()
                product.is_active = False
                product.save()
                return redirect('products')
            else:
                context['error'] = "Неправильный код!"

        context['col'] = col_list
        html_template = loader.get_template('home/products/product-detail.html')
        return HttpResponse(html_template.render(context, request))
    else:
        return redirect('products')


@login_required(login_url="/login/")
def product_add(request):
    context = {
        'segment': 'product',
        'form': {
            'client': {
                'first_name': '',
                'last_name': '',
                'email': '',
                'phone': '',
            },
            'product': {
                'name': '',
                'image': '',
                'comment': '',
                'height': '',
                'width': '',
                'length': '',
                'weight': '',
            }
        }
    }

    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        p_name = request.POST['p_name']

        p_image = None
        if request.FILES:
            p_image = request.FILES['p_image']
        p_comment = request.POST['p_comment']
        b_height = request.POST['b_height']
        b_weight = request.POST['b_weight']
        b_width = request.POST['b_width']
        b_length = request.POST['b_length']
        context['form']['client']['email'] = email
        context['form']['client']['first_name'] = first_name
        context['form']['client']['last_name'] = last_name
        context['form']['client']['phone'] = phone
        if email and first_name and last_name and phone and p_name and b_height and b_weight and b_width and b_length:
            client_first = Client.objects.filter(email=email, first_name=first_name, last_name=last_name, phone=phone)
            client = client_first.first()
            if client:
                client = client
            else:
                client = Client.objects.create(email=email, first_name=first_name, last_name=last_name, phone=phone)
                client.save()

            product_code = Product.objects.all().last()
            code = '745685'
            if product_code:
                code = str(int(product_code.code) + 1)

            capacity = int(b_width) * int(b_height) * int(b_length)
            price = int(b_weight) * capacity

            product = Product.objects.create(code=code, name=p_name,
                                             description=p_comment, image=p_image,
                                             price=price, weight=b_weight,
                                             capacity=capacity, client=client)
            product.user = request.user
            product.save()

            key = ''.join(random.choices(string.digits, k=8))
            user_code = ClientCode.objects.create(product=product, code=key)
            user_code.save()

            column_list = Column.objects.filter(is_free=True)

            for i in range(len(column_list)):
                if capacity == 0:
                    break
                if capacity > column_list[i].free_capacity:
                    capacity -= column_list[i].free_capacity
                    column_product = ColumnProduct.objects.create(product=product, column=column_list[i],
                                                                  capacity=column_list[i].free_capacity)
                    column_list[i].free_capacity = 0
                    column_list[i].is_free = False
                    column_list[i].save()
                    column_product.save()
                else:
                    column_list[i].free_capacity -= capacity
                    column_list[i].save()
                    column_product = ColumnProduct.objects.create(product=product, column=column_list[i],
                                                                  capacity=capacity)
                    column_product.save()
                    capacity = 0

            if capacity != 0:
                context['error'] = "Место нет!!"
            else:
                return redirect('product-detail', pk=product.id)
        else:
            context['error'] = "Заполните все поля!"

    html_template = loader.get_template('home/products/add-product.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def notFound(request):
    context = {}
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
