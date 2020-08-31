from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('info_list', views.info_list, name='info_list'),
    path('object_list', views.object_list, name='object_list'),
    path('champion_list', views.champion_list, name='champion_list'),    
]