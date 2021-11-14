from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag

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

class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'
    
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


