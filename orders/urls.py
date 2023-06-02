from django.urls import path
from .views import OrderCreateSubmitView

urlpatterns = [
    path('create/', OrderCreateSubmitView.as_view(), name='order_create'),
]