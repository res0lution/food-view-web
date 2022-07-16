from django.urls import path

from . import views

urlpatterns = [
    path('meal', views.meal, name='meal'),
    path('meal/add', views.add_meal, name='add_meal'),
    path('meal/edit/<int:meal_id>', views.edit_meal, name='edit_meal'),
]