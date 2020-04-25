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
    status_temp = apps.get_app_config('weather_app').status_temp
    status_press = apps.get_app_config('weather_app').status_press
    status_vis = apps.get_app_config('weather_app').status_vis
    status_hum = apps.get_app_config('weather_app').status_hum
    display_list = apps.get_app_config('weather_app').display_list
    empty_cells = 4 - len(list_of_cities)
    context_variables = {'display_list':display_list,'dates': list_of_dates, 'cities': list_of_cities, 'range': range(empty_cells),
                         'list_for_graph': list_for_graph,'status_temp': status_temp,'status_press': status_press,'status_hum': status_hum,'status_vis': status_vis}
    return render(request, 'weather_app/base.html', context_variables)


@csrf_protect
def search_city(request):
    url_api = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=24fa72dcfd34b9a33c1b1c518534a45b'
    city_name = request.POST.get('pretraga')
    r = requests.get(url_api.format(city_name)).json()
    if r['cod'] == '404':
        return redirect('base')
    else:
        dict_of_dates = format_api_response(r)
        if len(apps.get_app_config('weather_app').list_of_dates) > 0:
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
        city = City(city_name, dict_of_dates, stats)
        graph = initialize_graph_data(city)
        city.graph = graph
        if city in apps.get_app_config('weather_app').list_of_cities:
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


    for city in apps.get_app_config('weather_app').list_for_graph:
        for key in city_name:
            if key == city.name:
                apps.get_app_config('weather_app').list_for_graph.remove(city)

    return redirect('base')


@csrf_protect
def change_stats(request):
    if request.POST.get('temperature'):
        apps.get_app_config('weather_app').status_temp = 'red'
        apps.get_app_config('weather_app').status_press = 'blue'
        apps.get_app_config('weather_app').status_hum = 'blue'
        apps.get_app_config('weather_app').status_vis = 'blue'
        apps.get_app_config('weather_app').display_list = 'temperature'
    elif request.POST.get('pressure'):
        apps.get_app_config('weather_app').status_temp = 'blue'
        apps.get_app_config('weather_app').status_press = 'red'
        apps.get_app_config('weather_app').status_hum = 'blue'
        apps.get_app_config('weather_app').status_vis = 'blue'
        apps.get_app_config('weather_app').display_list = 'pressure'
    elif request.POST.get('humidity'):
        apps.get_app_config('weather_app').status_temp = 'blue'
        apps.get_app_config('weather_app').status_press = 'blue'
        apps.get_app_config('weather_app').status_hum = 'red'
        apps.get_app_config('weather_app').status_vis = 'blue'
        apps.get_app_config('weather_app').display_list = 'humidity'
    elif request.POST.get('visibility'):
        apps.get_app_config('weather_app').status_temp = 'blue'
        apps.get_app_config('weather_app').status_press = 'blue'
        apps.get_app_config('weather_app').status_hum = 'blue'
        apps.get_app_config('weather_app').status_vis = 'red'
        apps.get_app_config('weather_app').display_list = 'visibility'
    else:
        return redirect('base')
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
                    stats = Stats(date, element['main']['temp'], element['main']['temp_max'],
                                  element['main']['temp_min'], element['main']['feels_like'],
                                  element['main']['pressure'], element['clouds']['all'], element['main']['humidity'],
                                  element['weather'][0]['description'])
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
        for key, value in city.dict_of_dates[element].items():
            time_list.append(key)
            temperature_list.append(value.temp)
            humiditiy_list.append(value.humidity)
            pressure_list.append(value.pressure)
            visibility_list.append(value.clouds)
    graph = Graph_data(time_list, temperature_list, humiditiy_list, pressure_list, visibility_list)
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
