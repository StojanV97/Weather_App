import json
import os


from django.db import models


class City(object):
    __slots__ = '_name', '_dict_of_dates'

    def __init__(self,name,dict_of_dates):
        self._dict_of_dates = dict_of_dates
        self._name = name



class Stats(object):
    __slots__ = '_temp', '_feels_like', '_temp_min', '_temp_max', '_pressure','_humidity','_weather'

    def __init__(self,temp,temp_max,temp_min,feels_like,pressure,humidity,weather):
        self._temp = temp
        self._temp_max = temp_max
        self._feels_like = feels_like
        self._temp_min = temp_min
        self._pressure = pressure
        self._humidity = humidity
        self._weather = weather

    def __str__(self):
        return '{},{},{},{},{}'.format(self._temp,self._temp_max,self._temp_min,self._feels_like,self._weather)