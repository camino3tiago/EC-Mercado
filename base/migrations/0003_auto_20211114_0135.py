# Generated by Django 3.2.9 on 2021-11-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='sub_quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='sub_unit',
            field=models.IntegerField(blank=True, choices=[(1, '個'), (2, 'g'), (3, 'ml'), (4, '本'), (4, 'パック'), (5, '袋'), (6, '切れ'), (7, '枚'), (8, '玉'), (9, '束'), (10, '房')], null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='unit',
            field=models.IntegerField(choices=[(1, '個'), (2, 'g'), (3, 'ml'), (4, '本'), (4, 'パック'), (5, '袋'), (6, '切れ'), (7, '枚'), (8, '玉'), (9, '束'), (10, '房')], default=1),
        ),
    ]