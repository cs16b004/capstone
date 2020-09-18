from django.db import models
import datetime
import uuid
import time
# Create your models here.
class Order(models.Model):
	TYPE_CHOICES = [("LM", "Limit"),("MR","Market"),]
	CAT_CHOICES  = [("Buy","Buy"), ("Sell","Sell")]
	order_id           = models.UUIDField(editable=False, default=uuid.uuid4)
	order_category     = models.CharField(null=False,blank=False, max_length=10, choices = CAT_CHOICES)
	order_time         = models.DateTimeField(editable=False, default=datetime.datetime.now)
	order_quantity     = models.IntegerField(null=False, blank=False ,default =100)
	order_type         = models.CharField(null=False,blank=False, choices = TYPE_CHOICES, max_length=10,default = "MR")
	order_price        = models.FloatField(null=False,blank=False,default = 100)
	#No_extra           = models.BooleanField(null=False,blank=False,default = True)
	All_or_none        = models.BooleanField(null=True,blank=True)
	Minimum_fill       = models.IntegerField(null=True,blank=True)
	Disclosed_Quantity = models.IntegerField(null=True, blank=True)
	user_id            = models.CharField(null=False, blank=False, max_length=100, default = 'YAUID')
	order_status       = models.CharField(editable=False, max_length=10, default='Waiting')
	traded_quantity    = models.IntegerField(null = False, editable=False, default = 0)
	trade_price_list   = models.TextField(null = False, editable=False, default = '',max_length=200)
	trade_quant_list   = models.TextField(null = False, editable=False, default = '',max_length=200)
	trade_id           = models.CharField(null = False, editable=False, default='',max_length=100)
	user_all           = models.BooleanField(null = False, editable=False, default =False)
	user_MinFill       = models.BooleanField(null = False, editable=False, default =False)
	user_disclosed     = models.BooleanField(null=False, editable =False,default=False)

	def net_quantity(self):
		if (self.order_quantity - self.traded_quantity) >= self.Disclosed_Quantity:
			return self.Disclosed_Quantity - (self.traded_quantity % self.Disclosed_Quantity)
		else:
			return self.order_quantity - self.traded_quantity


class TradePrice(models.Model):
	last_trade_price = models.FloatField(editable=False,null=False,blank=False,default = 100)
	last_trade_day   = models.DateTimeField(editable=False,null=False, default=datetime.date.today)






"""class Order-temp:

    def __init__(self, quantity, order_type, price, All_or_none=False, Minimum_fill=0, Disclosed_Quantity=0):
    self.order_id           = uuid4()
    self.order_time         = datetime.now()
    self.quantity           = quantity
    self.order_type         = order_type
    self.price              = price
    self.All_or_none        = All_or_none
    self.Minimum_fill       = Minimum_fill
    self.Disclosed_Quantity = Disclosed_quantity
"""
