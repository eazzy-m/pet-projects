from decimal import Decimal
from django.urls import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def get_count_model_inst(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_good_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class ShowGoodsManager:

    @staticmethod
    def get_goods_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        goods = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_goods = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            goods.extend(model_goods)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        goods, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return goods


class ShowGoods:
    objects = ShowGoodsManager()


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


class CountManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_count_good_in_cat(self):
        models = get_count_model_inst('mobtel', 'television')
        good_in_cat = list(self.get_queryset().annotate(*models).values())
        return good_in_cat


class CategoryGoods(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название товарной категории')
    slug = models.SlugField(unique=True)
    cat_goods_cat_second = models.ForeignKey(CategorySecond, related_name='category_goods',
                                             on_delete=models.CASCADE, blank=True, null=True)
    objects = CountManager()

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
        return self.title

    def get_absolut_url(self):
        return get_good_url(self, 'good_detail')

    # @property
    # def stock_availability(self):
    #     if self.stock_availability:
    #         return 'Да'
    #     else:
    #         return 'Нет'


class Television(Good):
    Release_date = models.DateField(auto_now_add=False, verbose_name='Дата Выхода')
    stock_availability = models.BooleanField(default=True, verbose_name="Наличие на сладе")
    o_s = models.CharField(max_length=30, verbose_name='Версия системы')
    screen_resolution = models.IntegerField(default=1, verbose_name='Разрешение экрана')

    class Meta:
        verbose_name = _('Television')
        verbose_name_plural = _('Televisions')

    def __str__(self):
        return f'{self.title}'

    def get_absolut_url(self):
        return get_good_url(self, 'good_detail')


class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='User')
    goods = models.ManyToManyField('Goods_in_basket', blank=True, related_name='related_basket')
    quantity_goods_basket = models.PositiveIntegerField(default=0)
    total_price_basket = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=Decimal("0.00"), verbose_name='Общая цена корзины')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        basket_data = self.goods_in_basket.aggregate(models.Sum('total_price'), models.Count('id'))
        if basket_data['total_price__sum']:
            self.total_price_basket = basket_data['total_price__sum']
        else:
            self.total_price_basket = 0
        self.quantity_goods_basket = basket_data['id__count']
        super().save(*args, **kwargs)


class Goods_in_basket(models.Model):
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, verbose_name='Корзина',
                               related_name='goods_in_basket')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=1, verbose_name='Количество')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,
                                      default=Decimal("0.00"), verbose_name='Общая цена')

    def __str__(self):
        return f'{self.basket}--{self.content_object.title}--{self.count}'

    def save(self, *args, **kwargs):
        self.total_price = self.count * self.content_object.price
        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    status = models.CharField(max_length=32, verbose_name='Статус', default='в процессе')

    def __str__(self):
        return f'{self.status, self.user}'
