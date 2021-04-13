from django.urls import path, include
from catalog.views import main, GoodDetailView




urlpatterns = [
    path('', main, name='main'),
    path('goods/<str:ct_model>/<str:slug>/', GoodDetailView.as_view(), name='good_detail'),
]