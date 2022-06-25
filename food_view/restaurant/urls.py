from django.urls import path

from . import views

urlpatterns = [
    path('meal', views.meal, name='meal'),
    path('meal/add', views.add_meal, name='add_meal'),
]