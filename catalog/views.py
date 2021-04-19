from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.models import User
from django.contrib import messages
from catalog.models import MobTel, Television, Basket, Goods_in_basket, \
    CategoryFirst, CategorySecond, CategoryGoods, Good
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from catalog.mixins import BasketMixin
from catalog.forms import OrderForm


def main(request):
    return render(request, 'main.html', {})


class GoodDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'mobtel': MobTel,
        'television': Television
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    template_name = 'catalog/good_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'good'

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(GoodDetailView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = {i.verbose_name.title().capitalize(): i.value_from_object(kwargs['object']) for i in
                                self.model._meta.get_fields()[7:]}
        return context


def category_first(request):
    category_electronics = CategoryFirst.objects.get(name='Электроника').category_second.all()
    category_comps = CategoryFirst.objects.get(name='Компьютеры и сети').category_second.all()

    return render(request, 'catalog/category_first.html', {'category_electronics': category_electronics,
                                                           'category_comps': category_comps
                                                           })


def category_name(request, slug):
    Cat = {
        'Мобильные телефоны': 'mobtel__count',
        'Телевизоры': 'television__count',
        'Наушники': 'Headphones__count',
        'ТВ-антенны': 'tv_antennas__count',
        'Ноутбуки': 'laptops__count',
        'Компьютреы': 'computers__count',
        'Видеокарты': 'video_cards__count',
        'Процессоры': 'processors__count',
    }
    list_data = CategoryGoods.objects.get_count_good_in_cat()
    categoryname = CategorySecond.objects.get(slug=slug).category_goods.all()
    category_name = []
    for i in categoryname:
        for k in list_data:
            if i.name in k.values():
                if Cat[i.name] in k:
                    category_name.append(dict(name=k['name'], slug=k['slug'], count=k[Cat[i.name]]))
                else:
                    category_name.append(dict(name=k['name'], slug=k['slug'], count=0))
    return render(request, 'catalog/category_name.html', {'category_name': category_name})


def category_goods(request, slug):
    mod = {
        'mobtel': MobTel,
        'television': Television
    }
    if slug in mod:
        model = globals().get(mod[slug].__name__)
        category_goods = model.objects.all()
        return render(request, 'catalog/category_goods.html', {
            'category_goods': category_goods,
            'slug': slug,
        })
    else:
        return render(request, 'catalog/category_goods.html', {
            'slug': slug,
        })


class AddGoodInBasket(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, good_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        good = content_type.model_class().objects.get(slug=good_slug)
        good_in_basket, created = Goods_in_basket.objects.get_or_create(
             basket=self.basket, content_type=content_type, object_id=good.id)
        messages.add_message(request, messages.INFO, "Товар добавлен")
        return HttpResponseRedirect('/basket/')


class DelGoodInBasket(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, good_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        good = content_type.model_class().objects.get(slug=good_slug)
        good_in_basket = Goods_in_basket.objects.get(
             basket=self.basket, content_type=content_type, object_id=good.id)
        good_in_basket.delete()
        self.basket.save()
        messages.add_message(request, messages.INFO, "Товар удален")
        return HttpResponseRedirect('/basket/')


class ChangeGoodInBasket(BasketMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, good_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        good = content_type.model_class().objects.get(slug=good_slug)
        good_in_basket = Goods_in_basket.objects.get(
             basket=self.basket, content_type=content_type, object_id=good.id)
        count = int(request.POST.get('count'))
        good_in_basket.count = count
        good_in_basket.save()
        self.basket.save()
        messages.add_message(request, messages.INFO, "Количество изменено")
        return HttpResponseRedirect('/basket/')


class BasketView(BasketMixin, View):

    def get(self, request, *args, **kwargs):

        goods_in_basket = Goods_in_basket.objects.filter(basket=self.basket).order_by('pk')
        context = {'basket': self.basket, 'goods_in_basket': goods_in_basket}
        return render(request, 'catalog/basket.html', context)


class MakingOrderView(BasketMixin, View):

    def get(self, request, *args, **kwargs):
        goods_in_basket = Goods_in_basket.objects.filter(basket=self.basket).order_by('pk')
        form = OrderForm(request.POST or None)
        context = {'basket': self.basket, 'goods_in_basket': goods_in_basket, 'form': form}
        return render(request, 'catalog/making_order.html', context)


class AddOrderView(BasketMixin, View):

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            goods_in_basket = Goods_in_basket.objects.filter(basket=self.basket)
            goods_in_basket.delete()
            return HttpResponseRedirect('/basket/')


