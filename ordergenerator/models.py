from django.db import models
import datetime
import uuid
import numpy as np
# Create your models here.
class Order(models.Model):
    TYPE_CHOICES = [("LM", "Limit"),("MR","Market"),]
    CAT_CHOICES  = [("Buy","Buy"), ("Sell","Sell")]
    order_id           = models.UUIDField(editable=False, default=uuid.uuid4)
    order_category     = models.CharField(blank=False, max_length=10, choices = CAT_CHOICES)
    order_time         = models.DateTimeField(editable=False, default=datetime.datetime.now)
    order_quantity     = models.IntegerField(blank=False)
    order_type         = models.CharField(blank=False, choices = TYPE_CHOICES, max_length=10)
    order_price        = models.IntegerField(blank=False)
    No_extra           = models.BooleanField(blank=False)
    All_or_none        = models.BooleanField(null=True,blank=True)
    Minimum_fill       = models.IntegerField(null=True,blank=True)
    Disclosed_Quantity = models.IntegerField(null=True, blank=True)
    order_status       = models.CharField(editable=False, max_length=10, )
    
class Generator():
    def __init__(self, duration=120, cat_prob=0.5, type_prob=0, noextra=False, price_avg=100, quantity_avg=100):
        self.duration      = duration
        self.cat_prob     = cat_prob
        self.type_prob    = type_prob
        self.noextra      = noextra
        self.price_avg    = price_avg
        self.quantity_avg = quantity_avg 
        print(self.noextra)
    def generate(self,  total):
        price_spread =      0.25
        quantity_spread =   5 
        #endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.duration)
        order_list = []
        for t in range(total):
            raw_price = np.random.normal(self.price_avg, price_spread)
            price     = round(raw_price - (raw_price*100%5)/100,2)
            quantity  = int(np.random.normal(self.quantity_avg,quantity_spread))
            o_type    = ("MR","LM")[self.type_prob < np.random.uniform()]
            o_cat     = ("Buy","Sell")[self.cat_prob < np.random.uniform()] 
            print(raw_price)
            Minimum_fill = np.random.randint(0,int(0.2*quantity))
            all_or_none  = np.random.choice(["True", "False"])
            dis_quant    = np.random.randint(0,int(0.2*quantity))
            order_list.append(Order(order_price        = price,\
                                    order_quantity     = quantity,\
                                    order_type         = o_type,\
                                    order_category     = o_cat,\
                                    No_extra           = self.noextra,\
                                    All_or_none        = all_or_none,\
                                    Disclosed_Quantity = dis_quant,\
                                    Minimum_fill       = Minimum_fill,))
        #for order in order_list:
        #    print(order.order_id,order.order_time, order.order_price, order.order_quantity)
        return order_list 
    """def start():
        price_spread =      0.25
        quantity_spread =   0.25 
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        while True:
            if datetime.datetime.now() >= endTime:
                raw_price = round(np.random.normal(self.price_avg,price_spread),2)
                price = raw_price - (raw_price*100%5)/100
                quantity = round(np.random.normal(self.quantity_avg,quantity_spread))
                
            else:    
                break
     return 0
    """
        







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