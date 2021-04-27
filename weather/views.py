from django.shortcuts import render, redirect
from .models import City
from .forms import WeatherForm
import requests
from django.http import HttpResponse
# Create your views here.


def index(request):
    appid = "05dbc256082a7009a810fb33346e517c"
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
                    }
        all_cities.append(city_info)
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():

                res = requests.get(url.format(value)).json()
                city_info = {
                'city': value,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
        form = WeatherForm()
        return render(request, 'weather/weather.html', {'city_info': city_info,
                                                        'all_info': all_cities,
                                                        'form': form})
    else:
        form = WeatherForm()
    context = {'all_info': all_cities,
               'form': form,
               }
    return render(request, 'weather/weather.html', context=context)


# def get_weather(request):
#     appid = "05dbc256082a7009a810fb33346e517c"
#     url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
#     if request.method == 'POST':
#         form = WeatherForm(request.POST)
#         if form.is_valid():
#             res = requests.get(url.format(form.name)).json()
#             city_info = {
#                 'city': form.name,
#                 'temp': res["main"]["temp"],
#                 'icon': res["weather"][0]["icon"]
#             }
#             return render(request, 'weather/weather.html', {'city_info': city_info})
#     else:
#         form = WeatherForm()
#     return render(request, 'weather/weather.html', {'form': form})


# weatherURL = "http://api.openweathermap.org/data/2.5/weather?"
