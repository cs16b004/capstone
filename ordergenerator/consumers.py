import json
from channels.generic.websocket import WebsocketConsumer
import numpy as np
from threading import Thread, Semaphore
import time
import datetime
from .models import Order
from .ordermatching import add_order, get_market_data, get_clock



class Generator:
    def __init__(self, duration=100, cat_prob=0.5, type_prob=0.2, noextra=False, price_avg=100, quantity_avg=100):
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
        price_spread =      0.15
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
        if all_or_none:
            Minimum_fill = quantity
            dis_quant = quantity
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
                time.sleep(0.5)
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
                add_order(order)
                #recent_order['order_count'] += 1
                #recent_order['latest_order'] = new_order
                #print('updated - order')
                #sem.release()
            else:
                #recent_order['time_out'] = True
                print('Time Over')
                break
        return 0


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        t = Thread(target = self.start_gen,)
        t.start()
        print('Conection successful')

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(self.scope["path"])
        text_data_json = json.loads(text_data)
        print("Text data received : ",text_data)
        message = text_data_json['message']
        #print(message)
       # t = Thread(target = self.start_gen,)
        #t.daemon  = True
       # t.start()
        #start_gen()
         #print(self)
    def start_gen(self):
        #g1 = Generator()
        #ol = g1.generate()
        my_clock = 0
        while True:
            #time.sleep(2)
            k = get_clock()
            if my_clock < k:
                my_clock = k
                b_orders, s_orders = get_market_data()
                lis1 = []
                lis2 = []
                for key in s_orders.keys(): 
                    lis2.append(key)
                for key in b_orders.keys(): 
                    lis1.append(key)
                lis1.sort()
                lis2.sort()
                top_buy_prices = (lis1,lis1[-5:])[len(lis1) > 5]
                top_sell_prices = (lis2,lis2[-5:])[len(lis2) > 5]
                i=0
                for price in top_buy_prices:
                    self.send(text_data=json.dumps({
                        'row'      : str(i),
                        'price'    : str(price),
                        'quantity' : str(b_orders[price]["total"]),
                        'num'      : str(len(b_orders[price]["orders"])),
                        'category' : 'Buy',

                    }))
                    i = i+1
                i=0
                print(s_orders)
                for price in top_sell_prices:
                    self.send(text_data=json.dumps({
                        'row'      : str(i),
                        'price'    : str(price),
                        'quantity' : str(s_orders[price]["total"]),
                        'num'      : str(len(s_orders[price]["orders"])),
                        'category' : 'Sell',

                    }))
                    i= i+1
                print('sent')
            else:
                time.sleep(1)
            #else:
            #    print('Already up to date')
            #    time.sleep(2)
            #else:
            #    print('waiting for new order')

        print(self.scope["path"])

        print('sent')
