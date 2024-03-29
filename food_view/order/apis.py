import json
from datetime import timedelta

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
    orders = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
        many=True
    ).data
    
    return JsonResponse({
        "orders": orders
    })

@csrf_exempt
def driver_pick_order(request):
    """
        params:
        access_token
        order_id
        return:
            {"status", "success"}
    """

    if request.method == 'POST':
        access_token = AccessToken.objects.get(
            token=request.POST.get('access_token'), 
            expires__gt = timezone.now()
        )

        driver = access_token.user.driver

        if Order.objects.filter(driver=driver, status=Order.ONTHEWAY):
            return JsonResponse({
                "status": "failed",
                "error": "Your outstanding order is not delivered yet"
            })

        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.STATUS
            )

            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({ "status": "success" })
        except Order.DoesNotExist:
            return JsonResponse({
                "status": "failed",
                "error": "This order has been picked up by another"
            })

def driver_get_latest_order(request):
    access_token = AccessToken.objects.get(
        token=request.GET['access_token'], 
        expires__gt = timezone.now()
    )

    driver = access_token.user.driver

    order = OrderSerializer(
        Order.objects.filter(driver=driver, status=Order.ONTHEWAY).last()
    ).data

    return JsonResponse({
        "order": order
    })

@csrf_exempt
def driver_complete_order(request):
    """
        params:
        access_token
        order_id
        return:
            {"status", "success"}
    """

    if request.method == 'POST':
        access_token = AccessToken.objects.get(
            token=request.POST.get('access_token'), 
            expires__gt = timezone.now()
        )

        driver = access_token.user.driver

        order = Order.objects.get(
            id = request.POST["order_id"],
            driver = None,
        )

        order.status = Order.DELIVERED
        order.save()

        return JsonResponse({ "status": "success" })

def driver_get_revenue(request):
    access_token = AccessToken.objects.get(
        token=request.POST.get('access_token'), 
        expires__gt = timezone.now()
    )

    driver = access_token.user.driver

    
    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({ "revenue": revenue })