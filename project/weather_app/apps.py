import json
import os


from django.apps import AppConfig




class WeatherAppConfig(AppConfig):
    name = 'weather_app'
    list_of_cities = []
    list_of_dates = []
    list_for_graph = []


