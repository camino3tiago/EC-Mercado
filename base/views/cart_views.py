from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict

class CartListView(ListView):
    model = Item
    template_name = 'pages/cart.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
        self.queryset = []
        self.total = 0
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total = obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        return super().get_queryset()
        

class AddCartView(View):
    
    # postメソッドでrequestが送信されてきた場合の処理(cartに追加された場合)
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        # 
        cart = request.session.get('cart', None)
        if cart in None or len(cart) == 0:
            # OrderedDictはpython標準のライブラリで、辞書を追加順に並べるために使用
            items = OrderedDict()   # インスタンス化
            cart = {'items': items}
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        request.session['cart'] = cart
        return redirect('/cart/')
        
    
