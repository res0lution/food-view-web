"""food_view URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from restaurant import apis as restaurant_apis
from order import apis as order_apis

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('restaurant/', include('order.urls')),

    path('api/socials/', include('rest_framework_social_oauth2.urls')),
    path('api/restaurant/order/notification/<last_request_time>/', order_apis.order_notification),

    path('api/customer/restaurants/', restaurant_apis.customer_get_restaurants),
    path('api/customer/meals/<int:restaurant_id>', restaurant_apis.customer_get_meals),
    path('api/customer/order/add', order_apis.customer_add_order),
    path('api/customer/order/latest', order_apis.customer_get_latest_order),
]
