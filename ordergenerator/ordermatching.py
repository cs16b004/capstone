from ordergenerator.models import Order
from heapq import heappush, heappop
import threading
total_orders = {'Buy' : {'MR': {}, 'LM': {}}, 'Sell': {'MR': {}, 'LM': {}}}
traded_orders = {'Buy' : {'MR': {}, 'LM': {}}, 'Sell': {'MR': {}, 'LM': {}}}
market_orders = {'orders': []}
buy_heap    = []
sell_heap   = []
buy_orders  = {}
sell_orders = {}
all_orders  = 0 

sem = threading.Lock()

def get_time(order):
	return order.order_time

def add_order(order):
	limit_price = order.order_price 
	if order.order_type == "MR":
		print("Market order added")
		market_orders["orders"].append(order)
		market_orders["orders"].sort(key = get_time)
		# return '-1'
	else:
		sem.acquire()
		global all_orders
		all_orders = all_orders + 1
		if order.order_category=='Buy':
			if limit_price not in buy_orders:
				heappush(buy_heap,-1*limit_price) #Max price on the top
				buy_orders[limit_price]={"orders":[],"total":0, "disclosed":0}
			buy_orders[limit_price]["orders"].append(order)
			buy_orders[limit_price]["orders"].sort(key = get_time)
			buy_orders[limit_price]["total"]+=order.net_quantity()
			buy_orders[limit_price]["disclosed"]+=order.Disclosed_Quantity
		else:
			if limit_price not in sell_orders:
				heappush(sell_heap, limit_price) #Min on top
				sell_orders[limit_price]={"orders":[],"total":0,"disclosed":0}
			sell_orders[limit_price]["orders"].append(order)
			sell_orders[limit_price]["orders"].sort(key = get_time)
			sell_orders[limit_price]["total"]+=order.net_quantity()
			sell_orders[limit_price]["disclosed"]+=order.Disclosed_Quantity
		sem.release()
		return order.order_id

def get_best_buy():
	sem.acquire()
	if len(buy_heap) > 0:
		top_buy_price                            = -1 * heappop(buy_heap)
	else:
		return -1
	order1                                   = buy_orders[top_buy_price]["orders"][0]
	buy_orders[top_buy_price]["orders"]      = buy_orders[top_buy_price]["orders"][1:]
	buy_orders[top_buy_price]["total"]   -= order1.net_quantity()
	buy_orders[top_buy_price]["disclosed"]  -= order1.Disclosed_Quantity
	sem.release()
	return order1

def get_best_sell():
	sem.acquire()
	if len(sell_heap) > 0:
		top_sell_price                           = heappop(sell_heap)
	else:
		return -1
	order2                                   = sell_orders[top_sell_price]["orders"][0]
	sell_orders[top_sell_price]["orders"]    = sell_orders[top_sell_price]["orders"][1:]
	sell_orders[top_sell_price]["total"] -= order2.net_quantity()
	sell_orders[top_sell_price]["disclosed"]  -= order2.Disclosed_Quantity
	sem.release()
	return order2

def get_orders_for_ordermatching():
	# check if any market orders are present
	# if market orders are present then make order1 as market order with least time stamp
	# order2 as limit order with best price available
	# else if no maket orders are present
	# make order1 as limit order with least time stamp
	# make order2 as limit order with same price and different category with least time stamp
	# return order1 and order2
	order1 = get_best_buy()
	order2 = get_best_sell()
	return order1, order2

#Make sure that order1 price >= order2 price if (order1 = buy, order2 = sell) respectively or vice versa
# if price dont match push them back using add orders function

def util_starter():
	orders = Order.objects.all().filter(order_status='Waiting')
	for order in orders:
		add_order(order)

	while True:
		if len(market_orders["orders"]) == 0:
			print('Executing Limit Order')
			order1, order2 = get_orders_for_ordermatching()
			if order1 != -1 and order2 != -1:
				if order1.order_price >= order2.order_price:
					match_orders_with_conditions(order1, order2)
			elif order1 == -1:
				print('No Buy orders to execute')
			elif order2 == -1:
				print('No sell orders to execute')
		else:
			print('Executing Market Order')
			order = market_orders['orders'][0]
			del market_orders['orders'][0]
			if order.order_category == 'Buy':
				order1 = order
				order2 = get_best_sell()
				if order2 != -1:
					match_orders_with_conditions(order1, order2)
				else:
					print('No sell orders to execute')
			else:
				order1 = get_best_buy()
				order2 = order
				if order1 != -1:
					match_orders_with_conditions(order1, order2)
				else:
					print('No Buy orders to execute')
		print(buy_heap)
		print(sell_heap)

def start_matcher():
	t = threading.Thread(target = util_starter)
	t.start()

def match_orders(order1, order2):
	if  order1.net_quantity() <= order2.net_quantity():
		order2.traded_quantity += order1.net_quantity()
		order1.traded_quantity = order1.order_quantity
		order1.order_status = 'Accepted'
		order1.save()
		order2.save()
		# Line to push the order1 to traded list of buy orders
		print('# Line to push the order1 to traded list of buy orders')
		if order1.net_quantity() == order2.net_quantity():
			# Line to push the order2 to the traded list of sell orders
            
			print('# Line to push the order2 to the traded list of sell orders')
		else:
			add_order(order2)
			# Line to push the order2 back to the sell orders heap
			print('# Line to push the order2 back to the sell orders heap')
	else:
		order1.traded_quantity += order2.net_quantity()
		order2.traded_quantity = order2.order_quantity
		order2.order_status = 'Accepted'
		order1.save()
		order2.save()
		add_order(order1)
		# Line to push the order2 to traded list of sell orders
		# Line to push the order1 back to the buy orders heap
		print('# Line to push the order2 to traded list of sell orders')
		print('# Line to push the order1 back to the buy orders heap')

def match_orders_with_conditions(order1, order2):
	order1_remaining = order1.net_quantity()
	order2_remaining = order2.net_quantity()
	if order1.Minimum_fill == 0:
		if (order2.traded_quantity !=0) or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill):
			match_orders(order1, order2)
		else:
			add_order(order2)
			add_order(order1)
	else:
		if (order1.traded_quantity != 0 and (order2.traded_quantity != 0 or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill))) or ((order1.traded_quantity == 0 and order2_remaining >= order1.Minimum_fill) and (order2.traded_quantity!=0 or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill))):
			match_orders(order1, order2)
		else:
			add_order(order2)
			add_order(order1)