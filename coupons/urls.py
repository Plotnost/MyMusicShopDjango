from django.urls import path
from .views import CouponApplyView


urlpatterns = [
    path('coupon/apply/', CouponApplyView.as_view(), name='apply'),
]