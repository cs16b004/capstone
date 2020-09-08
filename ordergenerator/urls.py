from django.urls import path
from . import views

urlpatterns = [
    path('order-page', views.order, name = 'order-page'),
    path('order/generator',views.startgenerate, name = 'generator')
]