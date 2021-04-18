from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.contrib.auth.models import User
from catalog.models import Basket


class BasketMixin(View):

    def dispatch(self, request, *args, **kwargs):
        self.basket = Basket.objects.get(user__username=request.user)
        self.basket.save()
        return super().dispatch(request, *args, **kwargs)

