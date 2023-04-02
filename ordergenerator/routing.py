from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/order/order/', consumers.OrderConsumer.as_asgi()),
    re_path('ws/order/order-test/', consumers.OrderConsumer.as_asgi()),
]
