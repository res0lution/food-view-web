from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/account/sign_in')
def home(request):
    return render(request, 'home.html', {})

def sign_up(request):
    return render(request, 'sign_up.html', {})