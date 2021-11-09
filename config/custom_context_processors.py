from django.conf import settings
from base.models import Item

# 全てのtemplateで共通に使えるcontextを定義できる

def base(request):
    items = Item.objects.filter(is_published=True)
    return {
        'TITLE': settings.TITLE,
        'ADDITIONAL_ITEMS': items,  # 追加アイテム(おすすめとして表示する)
        'POPULAR_ITEMS': items.order_by('-sold_count') # 人気アイテム
    }

