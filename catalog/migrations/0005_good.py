# Generated by Django 3.1.7 on 2021-04-09 18:33

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_categorygoods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Название')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Изображение')),
                ('descriptions', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=6, verbose_name='Цена')),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='good', to='catalog.categorygoods')),
            ],
        ),
    ]