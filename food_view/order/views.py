from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/account/sign_in')
def order(request):
    return render(request, 'order.html', {})

@login_required(login_url='/account/sign_in')
def report(request):
    return render(request, 'report.html', {})
