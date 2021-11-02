from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item

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
    