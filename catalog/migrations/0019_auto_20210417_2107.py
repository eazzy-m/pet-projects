# Generated by Django 3.1.7 on 2021-04-17 18:07

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_basket_goods'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='quantity_goods_basket',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='basket',
            name='total_price_basket',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Общая цена корзины'),
        ),
    ]
