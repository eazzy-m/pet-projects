from decimal import Decimal
from django.shortcuts import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CategoryFirst(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название главной категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class CategorySecond(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название второй категории')
    slug = models.SlugField(unique=True)
    cat_second_cat_first = models.ForeignKey(CategoryFirst, related_name='category_second',
                                             on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class CategoryGoods(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название товарной категории')
    slug = models.SlugField(unique=True)
    cat_goods_cat_second = models.ForeignKey(CategorySecond, related_name='category_goods',
                                             on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Good(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name='Изображение')
    about = models.CharField(max_length=50, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"), verbose_name='Цена')
    product_category = models.ForeignKey(CategoryGoods, on_delete=models.CASCADE, blank=True,
                                         null=True)


class MobTel(Good):
    Release_date = models.DateField(auto_now_add=False, verbose_name='Дата Выхода')
    stock_availability = models.BooleanField(default=True, verbose_name='Наличие на складе')
    o_s = models.CharField(max_length=30, verbose_name='Операционная система')
    screen_size = models.DecimalField(max_digits=2, decimal_places=1,
                                      default=Decimal("0.0"), verbose_name='Размер экрана')
    quant_sim = models.IntegerField(default=1, verbose_name='Количество симкарт')


    def __str__(self):
        return f'{self.title}'


class Television(Good):
    Release_date = models.DateField(auto_now_add=False, verbose_name='Дата Выхода')
    stock_availability = models.BooleanField(default=True, verbose_name="Наличие на сладе")
    o_s = models.CharField(max_length=30, verbose_name='Версия системы')
    screen_resolution = models.IntegerField(default=1, verbose_name='Разрешение экрана')


    def __str__(self):
        return f'{self.title}'


class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return self.user.username


class Goods_in_basket(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, verbose_name='Корзина')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=Decimal("0.00"), verbose_name='Общая цена')

    def __str__(self):
        return f'{self.basket}--{self.good.title}--{self.count}'


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    status = models.CharField(max_length=32, verbose_name='Статус', default='в процессе')

    def __str__(self):
        return f'{self.status, self.user}'


