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
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(user=self.request.user)
        return context


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
        context['orders'] = Order.objects.filter(user=self.request.user)
        context['items'] = json.loads(obj.items) 
        context['shipping'] = json.loads(obj.shipping)
        return context


import csv
def order_csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', '注文日時', '商品名', '商品価格', '数量', '税抜金額', '税込金額', '出荷日時', 'キャンセル日時',])
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        items = json.loads(order.items) 
        writer.writerow([order.id, order.created_at, " - ", " - ", " - ", order.amount, order.tax_included, order.shipped_at, order.canceled_at,])
        for item in items:
            writer.writerow(['', "", item['name'], item['price'], item['quantity'], "", "", "", "",])

    return response