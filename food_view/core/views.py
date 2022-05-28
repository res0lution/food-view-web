from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.forms import UserForm
from restaurant.forms import RestaurantForm

# Create your views here.

@login_required(login_url='/account/sign_in')
def home(request):
    return render(request, 'home.html', {})

def sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    return render(request, 'sign_up.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })