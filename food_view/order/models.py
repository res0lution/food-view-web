from django.db import models

from core.models import Customer, Driver
from restaurant.models import Restaurant, Meal
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered")
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="order_details")
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
