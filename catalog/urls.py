from django.urls import path, include
from catalog.views import main, GoodDetailView, category_first, category_name, category_goods, \
    BasketView, AddGoodInBasket, DelGoodInBasket, ChangeGoodInBasket, MakingOrderView,\
    AddOrderView, OrderView, add_feedback, feedback_list

urlpatterns = [
    path('', main, name='main'),
    path('goods/<str:ct_model>/<str:slug>/', GoodDetailView.as_view(), name='good_detail'),
    path('add_feedback/<str:ct_model>/<str:slug>/', add_feedback, name='add_feedback'),
    path('category_name/<str:slug>/', category_name, name='category_name'),
    path('category_goods/<str:slug>/', category_goods, name='category_goods'),
    path('category_first/', category_first, name='category_first'),
    path('basket/', BasketView.as_view(), name='basket'),
    # path('weather/', weather, name='weather'),
    path('add_good_in_basket/<str:ct_model>/<str:slug>/', AddGoodInBasket.as_view(), name='add_good_in_basket'),
    path('del_good_in_basket/<str:ct_model>/<str:slug>/', DelGoodInBasket.as_view(), name='del_good_in_basket'),
    path('making_order/', MakingOrderView.as_view(), name='making_order'),
    path('add_order/', AddOrderView.as_view(), name='add_order'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('feedback_list/<str:ct_model>/<str:slug>/', feedback_list, name='feedback_list'),
    path('change_good_in_basket/<str:ct_model>/<str:slug>/', ChangeGoodInBasket.as_view(),
         name='change_good_in_basket'),
]
