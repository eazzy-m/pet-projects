# Generated by Django 3.1.7 on 2021-04-17 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_remove_goods_in_basket_basket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='goods',
        ),
        migrations.AddField(
            model_name='goods_in_basket',
            name='basket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='goods_in_basket', to='catalog.basket', verbose_name='Корзина'),
            preserve_default=False,
        ),
    ]
