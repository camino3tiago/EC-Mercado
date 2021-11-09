from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Order
import json

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