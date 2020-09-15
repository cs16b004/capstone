import json
from channels.generic.websocket import WebsocketConsumer
import numpy as np
from threading import Thread, Semaphore
import time
import datetime
from .models import Order
from .ordermatching import add_order
sem = Semaphore(1)
recent_order = {\
    'time_out'    : False,\
    'order_count' : 0,\
    'latest_order' : {},\
}

class Generator:
    def __init__(self, duration=10, cat_prob=0.5, type_prob=0.2, noextra=False, price_avg=100, quantity_avg=100):
        self.duration     = duration
        self.cat_prob     = cat_prob
        self.type_prob    = type_prob
        self.noextra      = noextra
        self.price_avg    = price_avg
        self.quantity_avg = quantity_avg
#        print(self.noextra)
        my_thread         = Thread(target = self.start_generator)
        #my_thread.daemon  = True
        my_thread.start()
    def generate(self):
        price_spread =      0.25
        quantity_spread =   5
        #endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.duration)
        order_list = []
        #for t in range(total):
        raw_price = np.random.normal(self.price_avg, price_spread)
        price     = round(raw_price - (raw_price*100%5)/100,2)
        quantity  = int(np.random.normal(self.quantity_avg,quantity_spread))
        o_type    = ("MR","LM")[self.type_prob < np.random.uniform()]
        o_cat     = ("Buy","Sell")[self.cat_prob < np.random.uniform()]
        print(o_cat)
        Minimum_fill = np.random.randint(0,int(0.1*quantity))
        all_or_none  = np.random.choice(["True", "False"])
        dis_quant    = np.random.randint(int(0.2*quantity), quantity)
        # dis_quant = quantity
        new_order    = {"order_price"        : price,\
                           "order_quantity"     : quantity,\
                           "order_type"         : o_type,\
                           "order_category"     : o_cat,\
                           "All_or_none"        : all_or_none,\
                           "Disclosed_Quantity" : dis_quant,\
                           "Minimum_fill"       : Minimum_fill,\
                           "user_id"            : 'Generator'}
        #for order in order_list:
        #    print(order.order_id,order.order_time, order.order_price, order.order_quantity)
        return new_order
    def start_generator(self):
        endTime = datetime.datetime.now() + datetime.timedelta(seconds=self.duration)
        while True:
            if datetime.datetime.now() < endTime:
                time.sleep(0.2)
                new_order = self.generate()
                #sem.acquire()
                if new_order['order_type'] == 'MR':
                    new_order['order_price']        = -1
                    new_order['All_or_none']        = False                 #Default if not specified
                    new_order['Minimum_fill']       = 0                     #Default if not specified
                    new_order['Disclosed_Quantity'] = new_order['order_quantity']
                order = Order.objects.create(order_price        = new_order['order_price'],\
                                     order_category     = new_order['order_category'],\
                                     order_type         = new_order['order_type'],\
                                     order_quantity     = new_order['order_quantity'],\
                                     All_or_none        = new_order['All_or_none'],\
                                     Minimum_fill       = new_order['Minimum_fill'],\
                                     Disclosed_Quantity = new_order['Disclosed_Quantity'],\
                                     user_id            = 'Generator',\
                                     order_status       = 'Waiting')
                # add_order(order)
                recent_order['order_count'] += 1
                recent_order['latest_order'] = new_order
                print('updated - order')
                #sem.release()
            else:
                recent_order['time_out'] = True
                print('Time Over')
                break
        return 0


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('Conection successful')

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(self.scope["path"])
        text_data_json = json.loads(text_data)
        print("Text data received : ",text_data)
        message = text_data_json['message']
        #print(message)
        self.start_gen()
        #print(self)
    def start_gen(self):
        #g1 = Generator()
        #ol = g1.generate()
        myorder_count = 0
        while not recent_order['time_out']:
            if myorder_count < recent_order['order_count']:
                myorder_count  = recent_order['order_count']
                ol = recent_order['latest_order']
                self.send(text_data=json.dumps({
                    'message'  : str(ol["order_price"]),
                    'price'    : str(ol["order_price"]),
                    'quantity' : str(ol["order_quantity"]),
                    'category' : ol["order_category"],

                }))
                print('sent')
            #else:
            #    print('waiting for new order')

        print(self.scope["path"])

        print('sent')
