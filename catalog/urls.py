from django.urls import path, include
from catalog.views import main, GoodDetailView, category_first, category_name, category_goods




urlpatterns = [
    path('', main, name='main'),
    path('goods/<str:ct_model>/<str:slug>/', GoodDetailView.as_view(), name='good_detail'),
    path('category_name/<str:slug>/', category_name, name='category_name'),
    path('category_goods/<str:slug>/', category_goods, name='category_goods'),
    path('category_first/', category_first, name='category_first'),
]