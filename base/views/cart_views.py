from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    # cartに追加されているitemだけをlistで返す
    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:  # cartに何も入っていなければトップページへ
            return redirect('/')

        self.queryset = []  # 元々あるquerysetを上書きしていく
        self.total = 0  # 合計金額
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk)
            obj.quantity = quantity # モデル登録用ではなく、template表示用の一時的な値としてobj.quantityを格納
            obj.subtotal = int(obj.price * quantity)  # 小計金額　同上
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1))
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        return super().get_queryset()   # 上のコードを実行した上で、親のget_queryset()を返す
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['total'] = self.total
            context['tax_included_total'] = self.tax_included_total
        except Exception:
            pass
        return context


class AddCartView(LoginRequiredMixin, View):

    # postメソッドでrequestが送信されてきた場合の処理(cartに追加された場合)
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        # cartというsessionがあれば値を取得、なければNone
        cart = request.session.get('cart', None)

        # まだ、一度も商品を追加していなければ、cart辞書を作成
        if cart is None or len(cart) == 0: 
            """
            # OrderedDict：python標準のライブラリで、順序付き辞書
            pythonのdict型オブジェクトは、要素の順番を保持しない(python3.7以降は同様の機能あり)
            """
            items = OrderedDict()   # インスタンス化（辞書を追加順に並べるために使用）
            cart = {'items': items} # cart ->> {'items': OrderedDict()}

        # item_pkがcartにあれば、（すでに追加済みのアイテムであれば）
        if item_pk in cart['items']:    
            cart['items'][item_pk] += quantity  # cart ->> {'items': OrderedDict([(item_pk, quantity合計])}
        # item_pkがcartになければ、（初めて追加するアイテムの場合）
        else:                   
            cart['items'][item_pk] = quantity   # cart ->> {'items': OrderedDict([(item_pk, quantity])}
        request.session['cart'] = cart  # cartというsessionに変数cart辞書を入れる
        return redirect('/cart/')
        
        
@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', None)
    # cartにアイテムがある場合のみ実行
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')
