from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from base.models import Item

class Review(models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    reviewer = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default='匿名ユーザーさん', related_name='reviews', verbose_name='評価ユーザー', )
    product = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE, verbose_name='レビュー商品', )
    rate = models.IntegerField(choices=RATING, default=3, verbose_name='評価', )
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='タイトル')
    comment = models.TextField(null=True, blank=True, verbose_name='コメント')
    commented_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')

    def __str__(self):
        return f"{self.product} by {self.reviewer}"

