from django.urls import path, include
from catalog.views import main



urlpatterns = [
    path('', main, name='main'),
]