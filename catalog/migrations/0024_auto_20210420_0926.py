# Generated by Django 3.1.7 on 2021-04-20 06:26

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('catalog', '0023_basket_in_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods_in_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='Общая цена')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods_in_order', to='catalog.order', verbose_name='Заказ')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.ManyToManyField(blank=True, related_name='related_order', to='catalog.Goods_in_order'),
        ),
    ]
