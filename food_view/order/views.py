from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order

# Create your views here.
@login_required(login_url='/account/sign_in')
def order(request):
    if request.method == 'POST':
        order = Order.objects.get(id=request.POST["id"])

        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.filter(restaurant=request.user.restaurant).order_by('-id')
    return render(request, 'order.html', {
        "orders": orders
    })

@login_required(login_url='/account/sign_in')
def report(request):
    return render(request, 'report.html', {})
