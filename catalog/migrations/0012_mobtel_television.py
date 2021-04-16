# Generated by Django 3.1.7 on 2021-04-10 14:31

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20210409_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Television',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('about', models.CharField(max_length=50, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Цена')),
                ('Release_date', models.DateField(verbose_name='Дата Выхода')),
                ('stock_availability', models.BooleanField(default=True, verbose_name='Наличие на сладе')),
                ('o_s', models.CharField(max_length=30, verbose_name='Версия системы')),
                ('screen_resolution', models.IntegerField(default=1, verbose_name='Разрешение экрана')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.categorygoods')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MobTel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('about', models.CharField(max_length=50, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Цена')),
                ('Release_date', models.DateField(verbose_name='Дата Выхода')),
                ('stock_availability', models.BooleanField(default=True, verbose_name='Наличие на складе')),
                ('o_s', models.CharField(max_length=30, verbose_name='Операционная система')),
                ('screen_size', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=2, verbose_name='Размер экрана')),
                ('quant_sim', models.IntegerField(default=1, verbose_name='Количество симкарт')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.categorygoods')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]