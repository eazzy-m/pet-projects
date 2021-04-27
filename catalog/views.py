from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.models import User
from django.contrib import messages
from catalog.models import MobTel, Television, Basket, Goods_in_basket, \
    CategoryFirst, CategorySecond, CategoryGoods, Good, Order, Goods_in_order, Feedback, Course
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from catalog.mixins import BasketMixin
from catalog.forms import OrderForm, MobtelForm, TelevisionForm, FeedBackForm
import statistics
import requests


def main(request):
    url = 'https://www.nbrb.by/api/exrates/rates/145'
    res = requests.get(url).json()['Cur_OfficialRate']
    if not Course.objects.exists():
        cours = Course.objects.create()
        cours.course = res
        cours.save()
    else:
        cours = Course.objects.first()
        cours.course = res
        cours.save()
    models = [MobTel, Television]
    for j in models:
        for i in j._base_manager.all():
            i.price_in_d = float(i.price) / res
            i.save()
    messages.add_message(request, messages.INFO, "Курс доллара обновлен")
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
        ct_model = kwargs['object'].product_category.slug
        good_slug = kwargs['object'].slug
        content_type = ContentType.objects.get(model=ct_model)
        good = content_type.model_class().objects.get(slug=good_slug)
        feedbacks = Feedback.objects.all().filter(object_id=good.id, content_type=content_type)
        context['q_feedbacks'] = len(feedbacks)
        if feedbacks:
            context['estimation'] = int(statistics.mean([i.estimation for i in feedbacks]))
        else:
            context['estimation'] = 3
        return context


def category_name(slug):
    cat = {
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
                if cat[i.name] in k:
                    category_name.append(dict(name=k['name'], slug=k['slug'], count=k[cat[i.name]]))
                else:
                    category_name.append(dict(name=k['name'], slug=k['slug'], count=0))
    return  category_name


def category_first(request):
    if CategoryFirst.objects.get_or_create(name='Электроника', slug='electronics')[1]:
        categoryelectronic = CategoryFirst.objects.get(name='Электроника', slug='electronics')
        mobtel_accessories = CategorySecond.objects.create(name='Мобильные телефоны и аксессуары',
                                                           slug='mobtel_accessories',
                                                           cat_second_cat_first=categoryelectronic)
        television_video = CategorySecond.objects.create(name='Телевидение и видео', slug='television_video',
                                                         cat_second_cat_first=categoryelectronic)
        CategoryGoods.objects.create(name='Мобильные телефоны', slug='mobtel',
                                     cat_goods_cat_second=mobtel_accessories)
        CategoryGoods.objects.create(name='Наушники', slug='Headphones',
                                     cat_goods_cat_second=mobtel_accessories)
        CategoryGoods.objects.create(name='Телевизоры', slug='television',
                                     cat_goods_cat_second=television_video)
        CategoryGoods.objects.create(name='ТВ-антенны', slug='tv_antennas',
                                     cat_goods_cat_second=television_video)
    category_electronics = CategoryFirst.objects.get(name='Электроника',
                                                     slug='electronics').category_second.all()
    if CategoryFirst.objects.get_or_create(name='Компьютеры и сети', slug='computers_networks')[1]:
        categorycomp = CategoryFirst.objects.get(name='Компьютеры и сети', slug='computers_networks')
        laptops_computers_monitors = CategorySecond.objects.create(name='Ноутбуки, компьютеры, мониторы',
                                                                   slug='laptops_computers_monitors',
                                                                   cat_second_cat_first=categorycomp)
        components = CategorySecond.objects.create(name='Комплектующие', slug='components',
                                                   cat_second_cat_first=categorycomp)
        CategoryGoods.objects.create(name='Ноутбуки', slug='laptops',
                                     cat_goods_cat_second=laptops_computers_monitors)
        CategoryGoods.objects.create(name='Компьютреы', slug='computers',
                                     cat_goods_cat_second=laptops_computers_monitors)
        CategoryGoods.objects.create(name='Видеокарты', slug='video_cards',
                                     cat_goods_cat_second=components)
        CategoryGoods.objects.create(name='Процессоры', slug='processors',
                                     cat_goods_cat_second=components)
    category_comps = CategoryFirst.objects.get(name='Компьютеры и сети',
                                               slug='computers_networks').category_second.all()
    category_name_mobtel_accessories = category_name('mobtel_accessories')
    category_name_television_video = category_name('television_video')
    category_name_laptops_computers_monitors = category_name('laptops_computers_monitors')
    category_name_components = category_name('components')
    return render(request, 'catalog/category_first.html', {
                               'category_electronics': category_electronics,
                               'category_comps': category_comps,
                               'category_name_mobtel_accessories': category_name_mobtel_accessories,
                               'category_name_television_video': category_name_television_video,
                               'category_name_laptops_computers_monitors': category_name_laptops_computers_monitors,
                               'category_name_components': category_name_components})


def category_goods(request, slug):
    mod = {'mobtel': MobTel, 'television': Television}
    form = {'mobtel': MobtelForm(), 'television': TelevisionForm()}
    if slug in mod:
        model = globals().get(mod[slug].__name__)
        form = form[slug]
        category_goods = model.objects.all()

        category_name = CategoryGoods.objects.get(slug=slug)

        if request.method == 'POST':
            cours = Course.objects.first()
            form = {'mobtel': MobtelForm, 'television': TelevisionForm}
            form = form[slug](request.POST, request.FILES)
            if form.is_valid():
                good = form.save(commit=False)
                good.product_category = category_name
                good.price_in_d = float(good.price) / cours.course
                good.save()
                messages.add_message(request, messages.INFO, "Товар добавлен")
                return redirect('good_detail', ct_model=slug, slug=good.slug)
        if str(request.user) == 'admin':
            user = True
        else:
            user = None
        return render(request, 'catalog/category_goods.html', {
            'category_goods': category_goods, 'category_name': category_name,
            'slug': slug, 'form': form, 'user': user,
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
        messages.add_message(request, messages.WARNING, "Товар удален")
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
            order.total_price = self.basket.total_price_basket
            order.quantity_goods_order = self.basket.quantity_goods_basket
            order.save()
            goods_in_basket = Goods_in_basket.objects.filter(basket=self.basket)
            for go in goods_in_basket:
                Goods_in_order.objects.create(order=order, content_type=go.content_type, object_id=go.object_id,
                                              content_object=go.content_object, count=go.count,
                                              total_price=go.total_price)
            goods_in_basket.delete()
            self.basket.save()
            messages.add_message(request, messages.INFO, "Заказ принят")
            return HttpResponseRedirect('/orders/')


class OrderView(View):

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user__username=request.user)
        order_list = {order: order.goods_in_order.all() for order in orders}
        context = {'orders': order_list}
        return render(request, 'catalog/orders.html', context)


def add_feedback(request, ct_model, slug):
    content_type = ContentType.objects.get(model=ct_model)
    good = content_type.model_class().objects.get(slug=slug)
    if request.method == 'POST':
        form = FeedBackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.content_type = content_type
            feedback.object_id = good.id
            feedback.save()
            messages.add_message(request, messages.INFO, "Отзыв добавлен")
            return redirect('feedback_list', ct_model=ct_model, slug=slug)
    else:
        form = FeedBackForm()
    return render(request, 'catalog/add_feedback.html',
                  {'form': form, 'ct_model': ct_model, 'slug': slug, 'good': good})


def feedback_list(request, ct_model, slug):
    content_type = ContentType.objects.get(model=ct_model)
    good = content_type.model_class().objects.get(slug=slug)
    feedbacks = Feedback.objects.all().filter(object_id=good.id, content_type=content_type)
    return render(request, 'catalog/feedback_list.html', {'feedbacks': feedbacks, 'good': good})
