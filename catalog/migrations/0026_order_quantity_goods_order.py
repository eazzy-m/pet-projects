# Generated by Django 3.1.7 on 2021-04-20 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0025_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity_goods_order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
