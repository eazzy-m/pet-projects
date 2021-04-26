from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.contrib.auth.models import User
from catalog.models import Basket


class BasketMixin(View):

    def dispatch(self, request, *args, **kwargs):

        if Basket.objects.filter(user__username=request.user):
            self.basket = Basket.objects.get(user__username=request.user)
            self.basket.save()
        else:
            if str(request.user) == 'AnonymousUser':
                user = User.objects.get_or_create(username='AnonymousUser')[0]
                self.basket = Basket.objects.create(user=user)
                self.basket.save()
            else:
                self.basket = Basket.objects.create(user=request.user)
                self.basket.save()
        return super().dispatch(request, *args, **kwargs)

