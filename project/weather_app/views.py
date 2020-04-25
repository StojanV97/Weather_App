import json
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_protect
from weather_app.models import Stats
from weather_app.models import City
from weather_app.models import Graph_data


def base(request):
    url_api = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=24fa72dcfd34b9a33c1b1c518534a45b'
    list_of_dates = apps.get_app_config('weather_app').list_of_dates
    list_of_cities = apps.get_app_config('weather_app').list_of_cities
    list_for_graph = apps.get_app_config('weather_app').list_for_graph
    print(len(list_for_graph))
    empty_cells = 4 - len(list_of_cities)
    context_variables = {'dates': list_of_dates, 'cities': list_of_cities,'range':range(empty_cells),'list_for_graph':list_for_graph}
    return render(request,'weather_app/base.html',context_variables)

@csrf_protect
def search_city(request):
     url_api = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=24fa72dcfd34b9a33c1b1c518534a45b'
     city_name = request.POST.get('pretraga')
     r = requests.get(url_api.format(city_name)).json()
     if r['cod'] == '404':
         return redirect('base')
     else:
         dict_of_dates = format_api_response(r)
         if len(apps.get_app_config('weather_app').list_of_dates) > 0 :
             pass
         else:
             for date in dict_of_dates:
                apps.get_app_config('weather_app').list_of_dates.append(date)
         stats = None
         for stat in dict_of_dates:
             for s in dict_of_dates[stat]:
                 stats = dict_of_dates[stat][s]
                 break
             break
         city = City(city_name,dict_of_dates,stats)
         graph = initialize_graph_data(city)
         city.graph = graph
         if city in  apps.get_app_config('weather_app').list_of_cities:
             return redirect('base')
         else:
             if len(apps.get_app_config('weather_app').list_of_cities) < 4:
                apps.get_app_config('weather_app').list_of_cities.append(city)
         return redirect('base')

@csrf_protect
def addcheck(request):
    list = apps.get_app_config('weather_app').list_for_graph
    city_name = request.POST
    for city in apps.get_app_config('weather_app').list_of_cities:
        for key in city_name:
            if city.name == key:
                if city in list:
                    pass
                else:
                    list.append(city)
    return redirect('base')

@csrf_protect
def delete_city(request):
    list = apps.get_app_config('weather_app').list_of_cities
    city_name = request.POST
    for city in apps.get_app_config('weather_app').list_of_cities:
        for key in city_name:
            if key == city.name:
                list.remove(city)
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
                    stats = Stats(date,element['main']['temp'],element['main']['temp_max'],element['main']['temp_min'],element['main']['feels_like'],element['main']['pressure'],element['clouds']['all'],element['main']['humidity'],element['weather'][0]['description'])
                    dict[element['dt_txt']] = stats
        dict_of_dates[d] = dict
    return dict_of_dates

def initialize_graph_data(city):
    time_list = []
    temperature_list = []
    humiditiy_list = []
    pressure_list = []
    visibility_list = []
    for element in city.dict_of_dates:
        for key,value in city.dict_of_dates[element].items():
            time_list.append(key)
            temperature_list.append(value.temp)
            humiditiy_list.append(value.humidity)
            pressure_list.append(value.pressure)
            visibility_list.append(value.clouds)
    graph = Graph_data(time_list,temperature_list,humiditiy_list,humiditiy_list,visibility_list)
    print(len(time_list))
    print(time_list)
    print(len(visibility_list))
    print(visibility_list)
    print(len(temperature_list))
    print(temperature_list)
    print(len(pressure_list))
    print(pressure_list)
    print(len(humiditiy_list))
    print(humiditiy_list)
    return graph