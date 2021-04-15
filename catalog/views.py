from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from catalog.models import MobTel, Television, Basket, Goods_in_basket, \
    CategoryFirst, CategorySecond, CategoryGoods, Good


def main(request):
    return render(request, 'main.html')


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
        print(context['some_data'])
        return context


def category_first(request):
    category_electronics = CategoryFirst.objects.get(name='Электроника').category_second.all()
    category_comps = CategoryFirst.objects.get(name='Компьютеры и сети').category_second.all()

    return render(request, 'catalog/category_first.html', {'category_electronics': category_electronics,
                                                           'category_comps': category_comps
                                                           })


def category_name(request, slug):
    category_name = CategorySecond.objects.get(slug=slug).category_goods.all()
    return render(request, 'catalog/category_name.html', {
        'category_name': category_name,
    })


def category_goods(request, slug):
    mod = {
        'mobtel': MobTel,
        'television': Television
    }
    if slug in mod:
        print(mod[slug].__name__)
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
