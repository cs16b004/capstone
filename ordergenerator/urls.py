from django.urls import path
from . import views
from . import ordermatching

urlpatterns = [
    path('order/order-page', views.order, name = 'order-page'),
    path('order/generator',views.startgenerate, name = 'generator'),
    path('order/order/', views.room, name='room'),
    path('order/order-test/', views.room_test, name='room-test'),
    path('ordermatcher/', views.startmatcher, name='order-matcher')
]
