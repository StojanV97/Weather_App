from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('search', views.search_city, name='search_city')

]
