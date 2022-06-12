from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/sign_in', auth_views.LoginView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('account/sign_out', auth_views.LogoutView.as_view(next_page='/'), name='sign_out'),
    path('account/sign_up', views.sign_up, name='sign_up'),
    path('account', views.account, name='account'),
    path('restaurant', views.home, name=''),
]