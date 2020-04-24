import json
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests

# Create your views here.
from django.views.decorators.csrf import csrf_protect
from weather_app.models import Stats

from weather_app.models import City


def base(request):
    url_api = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=24fa72dcfd34b9a33c1b1c518534a45b'
    context_variables = {}
    return render(request,'weather_app/base.html',context_variables)

@csrf_protect
def search_city(request):
     url_api = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=24fa72dcfd34b9a33c1b1c518534a45b'
     city_name = request.POST.get('pretraga')
     r = requests.get(url_api.format(city_name)).json()
     cod = r['cod']
     if int(cod) == 404:
         return redirect('base')
     else:
         dict_of_dates = format_api_response(r)
         for date in dict_of_dates:
             apps.get_app_config('weather_app').list_of_dates.append(date)
         list_of_dates = apps.get_app_config('weather_app').list_of_dates
         city = City(city_name, dict_of_dates)
         for d in dict_of_dates:
             print(d + ':')
             for x in dict_of_dates[d]:
                 print(dict_of_dates[d][x])
         apps.get_app_config('weather_app').list_of_cities.append(city)
         return redirect('base')



def format_api_response(r):
    dict_of_dates = {}
    for element in r['list']:
        date = element['dt_txt']
        niz = date.split()
        dict_of_dates[niz[0]] = {}


    for d in dict_of_dates:
        dict = {}
        for element in r['list']:
            date = element['dt_txt']
            niz = date.split()
            if element['dt_txt'] in dict:
                pass
            else:
                if niz[0] == d:
                    stats = Stats(element['main']['temp'],element['main']['temp_max'],element['main']['temp_min'],element['main']['feels_like'],element['main']['pressure'],element['main']['humidity'],element['weather'][0]['description'])
                    dict[element['dt_txt']] = stats
        dict_of_dates[d] = dict
    return dict_of_dates