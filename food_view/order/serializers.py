from rest_framework import serializers

from core.models import Customer, Driver
from restaurant.models import Restaurant, Meal
from .models import Order, OrderDetails

class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ('id', 'name', 'avatar', 'address')


class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ('id', 'name', 'avatar', 'car_model', 'plate_number')


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'phone', 'address')


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'name', 'price')

class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer()

    class Meta:
        model = OrderDetails
        fields = ('id', 'meal', 'quantity', 'sub_total')


class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many=True)
    status = serializers.ReadOnlyField(source="get_status_display")

    class Meta:
        model = Order
        fields = ('id', 'customer', 'restaurant', 'driver', 'order_details', 'total', 'status', 'address')


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source="get_status_display")

    class Meta:
        model = Order
        fields = ('id', 'status')

