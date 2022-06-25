from .models import Restaurant, Meal
from django import forms

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "phone", "address", "logo")

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ("restaurant",)
