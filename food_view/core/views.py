from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from core.forms import UserForm
from restaurant.forms import RestaurantForm

# Create your views here.

@login_required(login_url='/account/sign_in')
def home(request):
    return render(request, 'order.html', {})

def sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'order.html', {})

    return render(request, 'sign_up.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })

@login_required(login_url='/account/sign_in')
def account(request):
    return render(request, 'account.html', {})