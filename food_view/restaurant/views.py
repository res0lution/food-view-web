from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MealForm

# Create your views here.
@login_required(login_url='/account/sign_in')
def meal(request):
    return render(request, 'meal.html', {})

@login_required(login_url='/account/sign_in')
def add_meal(request):
    if request.method == 'POST':
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():
            meal = meal_form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()
    
    meal_form = MealForm()

    return render(request, 'add_meal.html', {
        "meal_form": meal_form
    })
