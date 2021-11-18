from django.db import models
from django.contrib.auth import get_user_model
import datetime
import pandas as pd

def custom_timestamp_id():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f')  # strftime(): 日付、時間から文字列への変換

# 注文履歴を作成するモデル
class Order(models.Model):
    id = models.CharField(default=custom_timestamp_id, editable=False, primary_key=True, max_length=50)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uid = models.CharField(editable=False, max_length=50)
    is_confirmed = models.BooleanField(default=False)   # PayがsuccessしたらTrueにする
    amount = models.PositiveIntegerField(default=0)
    tax_included = models.PositiveIntegerField(default=0)
    items = models.JSONField()  
    shipping = models.JSONField()   # 注文時点でのUserの住所(配送先)
    shipped_at = models.DateTimeField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(blank=True) # 管理側で見れるメモ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id
