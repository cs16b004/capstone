from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/order/order/', consumers.OrderConsumer),
    re_path('ws/order/order-test/', consumers.OrderConsumer),
]
