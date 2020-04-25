import json
import os
from django.db import models


class City(object):
    __slots__ = '_delete','_name', '_dict_of_dates', '_graph_stats','_show_on_graph','_display_stat'

    def __init__(self, name, dict_of_dates,display_stat):
        self._dict_of_dates = dict_of_dates
        self._name = name
        self._display_stat = display_stat
        self._show_on_graph = False
        self._delete = False
        self._graph_stats = None

    @property
    def graph(self):
        return self._graph_stats

    @graph.setter
    def graph(self,value):
        self._graph_stats = value
    @property
    def delete(self):
        return self._delete
    @property
    def display_stat(self):
        return self._display_stat
    @property
    def name(self):
        return self._name
    @property
    def dict_of_dates(self):
        return self._dict_of_dates
    def __hash__(self):
        return hash((self._dict_of_dates, self._name, self._show_on_graph))
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return self._name == other._name and self._show_on_graph == other._show_on_graph


class Stats(object):
    __slots__ = '_date','_temp', '_feels_like', '_temp_min', '_temp_max', '_pressure', '_humidity', '_clouds','_weather'

    def __init__(self,date, temp, temp_max, temp_min, feels_like, pressure, clouds,humidity, weather):
        self._date = date
        self._temp = round((temp -  273.15),2)
        self._temp_max = round((temp_max -  273.15),2)
        self._feels_like = round((temp_min -  273.15),2)
        self._temp_min = round((feels_like -  273.15),2)
        self._pressure = round((pressure * 0.07),2)
        self._humidity = humidity
        self._weather = weather
        self._clouds = clouds

    @property
    def clouds(self):
        return self._clouds
    @property
    def date(self):
        return self._date
    @property
    def temp(self):
        return self._temp

    @property
    def temp_min(self):
        return self._temp_min

    @property
    def temp_max(self):
        return self._temp_max

    @property
    def feels_like(self):
        return self._feels_like

    @property
    def pressure(self):
        return self._pressure

    @property
    def humidity(self):
        return self._humidity

    @property
    def weather(self):
        return self._weather

    def __str__(self):
        return '{},{},{},{},{}'.format(self._temp, self._temp_max, self._temp_min, self._feels_like, self._weather)


class Graph_data(object):
    __slots__ = '_time','_temperature','_humidity','_pressure','_visibility'

    def __init__(self,time,temp,hum,press,vis):
        self._temperature = temp
        self._visibility = vis
        self._humidity = hum
        self._pressure = press
        self._time = time

    @property
    def temperature_list(self):
        return self._temperature

    @property
    def visibility_list(self):
        return self._visibility

    @property
    def humidity_list(self):
        return self._humidity

    @property
    def pressure_list(self):
        return self._pressure

    @property
    def time_list(self):
        return self._time
