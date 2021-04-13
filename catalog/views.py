from django.shortcuts import render
from django.views.generic import DetailView
from catalog.models import MobTel, Television, Basket, Goods_in_basket


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
        context['some_data'] = {i.verbose_name.title(): i.value_from_object(kwargs['object']) for i in
                                self.model._meta.get_fields()[7:]}
        return context
