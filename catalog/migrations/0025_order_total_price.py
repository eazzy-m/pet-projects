# Generated by Django 3.1.7 on 2021-04-20 08:44

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_auto_20210420_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='Общая цена'),
        ),
    ]
