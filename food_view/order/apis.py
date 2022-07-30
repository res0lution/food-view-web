import json

from django.http import JsonResponse
from django.utils import timezone
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderDetails
from restaurant.models import Meal
from .serializers import OrderSerializer, OrderStatusSerializer

@csrf_exempt
def customer_add_order(request):
    """
        params:
        access_token
        restaurant_id
        address
        order_details (json format), example:
            [{"meal_id": 1, "quantity": 2}, {"meal_id": 2, "quantity": 3}]
        return:
            {"status", "success"}
    """

    if request.method == 'POST':
        access_token = AccessToken.objects.get(
            token=request.POST.get('access_token'), 
            expires__gt = timezone.now()
        )

        customer = access_token.user.customer

        if Order.objects.filter(customer=customer).exclude(status=Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last order must be completed"})

        if not request.POST['address']:
            return JsonResponse({"status": "failed", "error": "Address is required"})
        
        order_details = json.loads(request.POST["order_details"])

        order_total = 0

        for meal in order_details:
            if not Meal.objects.filter(id=meal["meal_id"], restairant_id=request.POST["restairant_id"]):
                return JsonResponse({"status": "failed", "error": "Meals must be in only one restaurant"})
            else:
                order_total = Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            order = Order.objects.create(
                customer=customer,
                restairant_id=request.POST["restairant_id"],
                total=order_total,
                status=Order.COOKING,
                address=request.POST["address"]
            )

            for meal in order_details:
                OrderDetails.objects.create(
                    order = order,
                    meal_id = meal["meal_id"],
                    quantity = meal["quantity"],
                    sub_total = Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                )

            return JsonResponse({"status": "success"})

    return JsonResponse({})

def customer_get_latest_order(request):
    """
        params:
        access_token
        return:
            data witl all details about order
    """
    access_token = AccessToken.objects.get(
        token=request.GET.get('access_token'), 
        expires__gt = timezone.now()
    )
    customer = access_token.user.customer

    order = OrderSerializer(
        Order.objects.filter(customer=customer).last()
    ).data

    return JsonResponse({ "last": order })


def customer_get_latest_order_status(request):
    """
        params:
        access_token
        return:
            data witl all details about order
    """
    access_token = AccessToken.objects.get(
        token=request.GET.get('access_token'), 
        expires__gt = timezone.now()
    )
    customer = access_token.user.customer

    order_status = OrderStatusSerializer(
        Order.objects.filter(customer=customer).last()
    ).data

    return JsonResponse({ "last_order_status": order_status })

def order_notification(request, last_request_time):
    notification = Order.objects.filter(
        restaurant=request.user.restaurant,
        created_at__gt=last_request_time
    ).count()

    return JsonResponse({"notification": notification})


def driver_get_ready_orders(request):
    return JsonResponse({})

def driver_pick_order(request):
    return JsonResponse({})

def driver_get_latest_order(request):
    return JsonResponse({})

def driver_complete_order(request):
    return JsonResponse({})

def driver_get_revenue(request):
    return JsonResponse({})