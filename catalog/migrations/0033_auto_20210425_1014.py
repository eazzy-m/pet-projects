# Generated by Django 3.1.7 on 2021-04-25 07:14

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20210425_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobtel',
            name='price_in_d',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8, verbose_name='Цена в долларах'),
        ),
        migrations.AlterField(
            model_name='television',
            name='price_in_d',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8, verbose_name='Цена в долларах'),
        ),
    ]