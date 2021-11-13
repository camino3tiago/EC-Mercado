from django.db import models
from django.utils.crypto import get_random_string
import os

# 22文字のidをランダムに生成する関数
def create_id():
    return get_random_string(22)

# -----------デプロイしないことを前提としたpathとなっている（staticとか）--------------------
# itemファイルのパスを返す関数
def upload_image_to(instance, filename):
    item_id = instance.id   # instance = モデルの各インスタンス(instance.id=item.idと同様)
    # staticフォルダの中のitemsフォルダのitem_idごとのフォルダの中のfilename
    return os.path.join('media', 'items', item_id, filename)
# -----------------------------------------------------------------------------------

class Tag(models.Model):
    # slugをidとする * slugは基本URLで使用するので、英字が望ましい
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Category(models.Model):
    # slugをidとする * slugは基本URLで使用するので、英字が望ましい
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
    UNIT_CHOICES = (
        (1, '個'),
        (2, 'g'),
        (3, 'ml'),
        (4, '本'),
        (4, 'パック'),
        (5, '袋'),
        (6, '切れ'),
        (7, '枚'),
        (8, '玉'),
        (9, '束'),
        (10, '房'),
    )
    id = models.CharField(default=create_id, primary_key=True, max_length=22, editable=False)
    name = models.CharField(default='', max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.IntegerField(choices=UNIT_CHOICES, default=1)
    sub_quantity = models.PositiveIntegerField(null=True, blank=True)
    sub_unit = models.IntegerField(null=True, blank=True, choices=UNIT_CHOICES)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(default='', blank=True)
    sold_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='', blank=True, upload_to=upload_image_to)
    # 参照していたcategoryが削除された場合、nullにする
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, )

    def __str__(self):
        return self.name

