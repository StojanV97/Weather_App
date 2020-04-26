import json
import os


from django.apps import AppConfig




class WeatherAppConfig(AppConfig):
    name = 'weather_app'
    list_of_cities = []
    list_of_dates = []
    list_for_graph = []
    display_list = 'temperature'
    status_temp = 'red'
    status_press = '#3477eb'
    status_vis = '#3477eb'
    status_hum = '#3477eb'
    range_x = 0
    range_y = 40


