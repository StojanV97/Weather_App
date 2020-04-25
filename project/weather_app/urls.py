from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('search', views.search_city, name='search_city'),
    path('delete', views.delete_city, name='delete_city'),
    path('addcheck',views.addcheck,name='addcheck'),
    path('changestats',views.change_stats,name="change_stats")

]
