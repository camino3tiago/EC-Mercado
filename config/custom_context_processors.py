from django.conf import settings
from base.models import Item
import datetime

# 全てのtemplateで共通に使えるcontextを定義できる

def base(request):
    items = Item.objects.filter(is_published=True)
    current_month = datetime.date.today().month
    if 3 <= current_month <= 5:
        season = 'spring'
    elif 6 <= current_month <= 8:
        season = 'summer'
    elif 9 <= current_month <= 11:
        season = 'autumn'
    else:
        season = 'winter'
    return {
        'TITLE': settings.TITLE,
        'ADDITIONAL_ITEMS': items,  # 追加アイテム(おすすめとして表示する)
        'POPULAR_ITEMS': items.order_by('-sold_count'), # 人気アイテム
        'SEASON': season
    }

