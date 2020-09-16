from django.contrib import admin

# Register your models here.
from .models import Order, TradePrice
admin.site.register(Order)
admin.site.register(TradePrice)