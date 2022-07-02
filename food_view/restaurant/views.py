from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import MealForm
from .models import Meal

# Create your views here.
@login_required(login_url='/account/sign_in')
def meal(request):
    meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
    return render(request, 'meal.html', { "meals": meals })

@login_required(login_url='/account/sign_in')
def add_meal(request):
    if request.method == 'POST':
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()
            return redirect(meal)
    
    meal_form = MealForm()

    return render(request, 'add_meal.html', {
        "meal_form": meal_form
    })

@login_required(login_url='/account/sign_in')
def edit_meal(request, meal_id):
    if request.method == 'POST':
        meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=meal_id))

        if meal_form.is_valid():
            meal_form.save()
            return redirect(meal)
    
    meal_form = MealForm(instance=Meal.objects.get(id=meal_id))

    return render(request, 'edit_meal.html', {
        "meal_form": meal_form
    })
