from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='customer')
    avatar = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, related_name='driver')
    avatar = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255, blank=True)
    plate_number = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()
