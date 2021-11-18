from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order
import json
from django.conf import settings
from django.http import HttpResponse

class OrderIndexView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'pages/orders.html'
    ordering = '-created_at'

    def get_queryset(self):
        # ログインユーザーが注文したもの
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'pages/order.html'

    def get_queryset(self):
        # ログインユーザーが注文したもの
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object() # 親のget_object()メソッドを使用して、objに注文情報を入れる(Order.objects.get(pk=pk))
        # json to dict
        context['items'] = json.loads(obj.items) 
        context['shipping'] = json.loads(obj.shipping)
        return context

from django_pandas.io import read_frame

class OrderCsvView(View):

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        order_items = Order.objects.filter(pk=pk).values_list('items', flat=True)
        print('---------------------------------')
        print(order_items.first)
        print('---------------------------------')
        df = read_frame(
            order,
            fieldnames=[
                'id', 'items', 'amount', 'tax_included', 'uid', 'shipping',
            ]
        )
        import numpy as np
        import pandas as pd

        # items_data = {}
        # df_json = pd.DataFrame(items_data, columns=[''])
        # storeddata = Order.putframe(df_json)
        # retrieveddataframe = storeddata.loadframe()        
        # print(retrieveddataframe)
        # print(f'\n{type(retrieveddataframe)}\n')
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Deiposition'] = 'attachment; filename=orders.csv'
        df.to_csv(path_or_buf=response, encoding='utf_8_sig', index=None)
        return response