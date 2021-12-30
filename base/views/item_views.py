from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin
from base.forms import ReviewForm
from base.models import Item, Category, Tag, Order, Review
from django.db.models import Avg, Count
import json

class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'

# IndexListViewを関数汎用ビューで記載
"""
def index(request):
    object_list = Item.objects.all()
    context = {
        'object_list': object_list,
    }
    return render(request,
        'pages/index.html',
        context
    )
"""

class ItemDetailView(DetailView, ModelFormMixin):
    model = Item
    template_name = 'pages/item.html'
    form_class = ReviewForm
    
    def get_initial(self):
        initial = super().get_initial()
        initial['product'] = Item.objects.get(id=self.kwargs['pk'])
        initial['reviewer'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = super().get_object()
        
        if self.request.user.is_authenticated:
            # 自分の注文（Orderオブジェクト）
            my_orders = Order.objects.filter(user=self.request.user)
            
            # アイテムを購入しているか確認のため、item_pkに、(None/pk)を入れる
            for order in my_orders:
                order_item = json.loads(order.items)
                if order_item[0]['pk'] == context['item'].id:
                    context['item_pk'] = order_item[0]['pk']


        # おすすめ商品（同じカテゴリー）
        context["recommended_items"] = Item.objects.filter(is_published=True, category=context["item"].category).exclude(id=context["item"].id)[:8]

        # レビュー（レビュー数、平均値含む）
        context['reviews'] = Review.objects.filter(product=context['item'])
        avg_reviews = context['reviews'].aggregate(average=Avg('rate'))
        cnt_reviews = context['reviews'].aggregate(count=Count('id'))
        if avg_reviews['average'] is not None:
            avg=float(avg_reviews['average'])
            context['avg_rate'] = avg
        if cnt_reviews["count"] is not None:
            cnt = int(cnt_reviews["count"])
            context['cnt_rate'] = cnt    
        return context
    
class CategoryListView(ListView):
    model = Item    # あるcategoryを持ったItemのリスト
    template_name = 'pages/list.html'
    paginate_by = 8

    def get_queryset(self):
        # print(self.kwargs)  # ->> {'pk': 'urlから受け取ったCategoryのslug'}
        # インスタンス変数として、self.categoryを作成(categoryのpkを受け取り、一致するCategoryモデルのオブジェクトを代入する)
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category #{self.category.name}'
        return context

class TagListView(ListView):
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 8

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Tag #{self.tag.name}'
        return context


