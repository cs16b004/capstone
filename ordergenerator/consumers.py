import json
from channels.generic.websocket import WebsocketConsumer
from .models import Generator
import time
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
        g1 = Generator()
        ol = g1.generate( total = 100)

        for i in range(100):
            time.sleep(0.5)
            print(ol[i]["order_category"])
            self.send(text_data=json.dumps({
                'message'  : str(ol[i]["order_price"]),
                'price'    : str(ol[i]["order_price"]),
                'quantity' : str(ol[i]["order_quantity"]),
                'category' : ol[i]["order_category"],

            }))
            print('sent',i)
        
        print(self.scope["path"])

        print('sent')