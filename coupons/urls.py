from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
    path('clear/', views.clear_coupons, name='clear_coupons'),
]
