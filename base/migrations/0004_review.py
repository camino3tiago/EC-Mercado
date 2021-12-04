# Generated by Django 3.2.9 on 2021-12-02 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20211114_0135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3, verbose_name='評価')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='タイトル')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='コメント')),
                ('commented_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='base.item', verbose_name='レビュー商品')),
                ('reviewer', models.ForeignKey(default='匿名ユーザーさん', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='評価ユーザー')),
            ],
        ),
    ]