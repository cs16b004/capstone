from ordergenerator.models import Order,TradePrice
from heapq import heappush, heappop
import threading
import time
import os
import csv
total_orders = {'Buy' : {'MR': {}, 'LM': {}}, 'Sell': {'MR': {}, 'LM': {}}}
traded_orders = {'Buy' : {'MR': {}, 'LM': {}}, 'Sell': {'MR': {}, 'LM': {}}}
market_orders = {'orders': [], 'wait-orders':[]}
buy_heap    = []
sell_heap   = []
buy_orders  = {}
sell_orders = {}
all_orders  = 0 
last_traded_price = 100 #TradePrice.objects.all().order_by('-last_trade_day')[0].last_trade_price
sem = threading.Lock()
sem2 = threading.Lock()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_time(order):
	return order.order_time

def add_order(order):
	#print(order.order_time)git 
	limit_price = order.order_price 
	if order.order_type == "MR":
		print("Market order added")
		market_orders["orders"].append(order)
		market_orders["orders"].sort(key = get_time)
		return order.order_id
		# return '-1'
	else:
		sem.acquire()
		global all_orders
		all_orders = all_orders + 1
		# print(all_orders)
		if order.order_category=='Buy':
			if limit_price not in buy_orders:
				heappush(buy_heap,-1*limit_price) #Max price on the top
				buy_orders[limit_price]={"orders":[],"total":0, "disclosed":0}
			elif -1*limit_price not in buy_heap:
				heappush(buy_heap, -1*limit_price)
			buy_orders[limit_price]["orders"].append(order)
			buy_orders[limit_price]["orders"].sort(key = get_time)
			buy_orders[limit_price]["total"]+=order.net_quantity()
			buy_orders[limit_price]["disclosed"]+=order.Disclosed_Quantity
		else:
			if limit_price not in sell_orders:
				heappush(sell_heap, limit_price) #Min on top
				sell_orders[limit_price]={"orders":[],"total":0,"disclosed":0}
			elif limit_price not in sell_heap:
				heappush(sell_heap, limit_price)
			sell_orders[limit_price]["orders"].append(order)
			sell_orders[limit_price]["orders"].sort(key = get_time)
			sell_orders[limit_price]["total"]+=order.net_quantity()
			sell_orders[limit_price]["disclosed"]+=order.Disclosed_Quantity
		sem.release()
		return order.order_id

def get_best_buy():
	sem.acquire()
	if len(buy_heap) > 0:
		# top_buy_price                            = -1 * heappop(buy_heap)
		top_buy_price = -1 * buy_heap[0]
		if len(buy_orders[top_buy_price]["orders"]) == 1:
			heappop(buy_heap)
	else:
		sem.release()
		return -1
	order1                                   = buy_orders[top_buy_price]["orders"][0]
	buy_orders[top_buy_price]["orders"]      = buy_orders[top_buy_price]["orders"][1:]
	buy_orders[top_buy_price]["total"]   -= order1.net_quantity()
	buy_orders[top_buy_price]["disclosed"]  -= order1.Disclosed_Quantity
	if len(buy_orders[top_buy_price]["orders"]) == 0:
		del buy_orders[top_buy_price]
	sem.release()
	return order1

def get_best_sell():
	sem.acquire()
	if len(sell_heap) > 0:
		# top_sell_price                           = heappop(sell_heap)
		top_sell_price = sell_heap[0]
		if len(sell_orders[top_sell_price]["orders"]) == 1:
			heappop(sell_heap)
	else:
		sem.release()
		return -1
	order2                                   = sell_orders[top_sell_price]["orders"][0]
	sell_orders[top_sell_price]["orders"]    = sell_orders[top_sell_price]["orders"][1:]
	sell_orders[top_sell_price]["total"] -= order2.net_quantity()
	sell_orders[top_sell_price]["disclosed"]  -= order2.Disclosed_Quantity
	if len(sell_orders[top_sell_price]["orders"]) == 0:
		del sell_orders[top_sell_price]
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
	#orders = Order.objects.all().filter(order_status='Waiting')
	#for order in orders:
	#	add_order(order)

	while True:
		if len(market_orders["orders"]) == 0:
			print('Executing Limit Order')
			order1, order2 = get_orders_for_ordermatching()
			if order1 != -1 and order2 != -1:
				if order1.order_price >= order2.order_price:
					match_orders_with_conditions(order1, order2)
				else:
					add_order(order1)
					add_order(order2)
			elif order1 == -1:
				print('No Buy orders to execute')
			elif order2 == -1:
				print('No sell orders to execute')
		else:
			print('Executing Market Order')
			order = market_orders['orders'][0]
			if order.order_category == 'Buy':
				order1 = order
				order2 = get_best_sell()
				if order2 != -1:
					del market_orders['orders'][0]
					match_orders_with_conditions(order1, order2)
				else:
					print('No sell orders to execute')
			else:
				order1 = get_best_buy()
				order2 = order
				if order1 != -1:
					del market_orders['orders'][0]
					match_orders_with_conditions(order1, order2)
				else:
					print('No Buy orders to execute')
		print(buy_heap)
		print(sell_heap)

def start_matcher():
	t = threading.Thread(target = util_starter)
	t.start()

def check_and_update_order_status(order1, order2):
	if order1.traded_quantity == order1.order_quantity:
		order1.order_status = 'Accepted'
		print('Add order1 to accepted trades list')
	elif order1.traded_quantity < order1.order_quantity:
		add_order(order1)
		print('Add order1 to buy order heap')
	else:
		print('Something wrong')

	if order2.traded_quantity == order2.order_quantity:
		order2.order_status = 'Accepted'
		print('Add order2 to accepted trades list')
	elif order2.traded_quantity < order2.order_quantity:
		add_order(order2)
		print('Add order2 to sell order heap')
	else:
		print('Something wrong')
	
	order1.save()
	order2.save()

def match_orders(order1, order2):
	if  order1.net_quantity() <= order2.net_quantity():
		order2.traded_quantity += order1.net_quantity()
		order2.trade_quant_list += str(order1.net_quantity()) + ' '
		order1.trade_quant_list += str(order1.net_quantity()) + ' '
		order1.traded_quantity += order1.net_quantity()
		order2.trade_price_list += str(order1.order_price) + ' '
		order1.trade_price_list += str(order2.order_price) + ' '
		check_and_update_order_status(order1, order2)
	else:
		order1.traded_quantity += order2.net_quantity()
		order1.trade_quant_list += str(order2.net_quantity()) + ' '
		order2.trade_quant_list += str(order2.net_quantity()) + ' '
		order2.traded_quantity += order2.net_quantity()
		order2.trade_price_list += str(order1.order_price) + ' '
		order1.trade_price_list += str(order2.order_price) + ' '
		check_and_update_order_status(order1, order2)

def not_satified_disclosed_quantity(order1, order2):
	if order1.order_type == 'MR':
		order = get_best_sell()
		if order != -1:
			match_orders_with_conditions(order1, order)
			print(order1.order_id)
			print(order.order_id)
		else:
			# add_order(order1)
			# Need to add market order somewhere
			print('error with sell order')
		add_order(order2)
	elif order2.order_type == 'MR':
		order = get_best_buy()
		if order != -1:
			match_orders_with_conditions(order, order2)
			print(order2.order_id)
			print(order.order_id)
		else:
			# add_order(order2)
			# Need to add market order somewhere
			print('error with buy order')
		add_order(order1)
	else:
		# time.sleep(2)
		order = get_best_sell()
		if order != -1:
			if order1.order_price >= order.order_price:
				match_orders_with_conditions(order1, order)
			else:
				add_order(order1)
			#add_order(order1)
			add_order(order2)
		else:
			add_order(order1)
			add_order(order2)

def match_orders_with_conditions(order1, order2):
	order1_remaining = order1.net_quantity()
	order2_remaining = order2.net_quantity()
	if order1.Minimum_fill == 0:
		if (order2.traded_quantity !=0) or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill):
			match_orders(order1, order2)
		else:
			not_satified_disclosed_quantity(order1, order2)
	else:
		if (order1.traded_quantity != 0 and (order2.traded_quantity != 0 or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill))) or ((order1.traded_quantity == 0 and order2_remaining >= order1.Minimum_fill) and (order2.traded_quantity!=0 or (order2.traded_quantity == 0 and order1_remaining >= order2.Minimum_fill))):
			match_orders(order1, order2)
		else:
			not_satified_disclosed_quantity(order1, order2)

def get_market_data(): 
	sem.acquire()
	k1=buy_orders
	k2=sell_orders
	sem.release()
	return k1,k2
def get_clock(): 
	if len(buy_heap) > 0 and len(sell_heap) > 0: 
		global all_orders
		return all_orders
	return 0
def get_last_price():
	return last_traded_price

def fill_excel(lst,filename,fields):
	path = os.path.join(BASE_DIR,'excel/')
	flag = os.path.exists(path)

	if flag == False :
		os.mkdir(path)

	with open(path+filename,'w',newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)
	for id in lst:
		order = Order.objects.get(order_id = id)
		print(id)
		order = vars(order)
		values = list(order.values())
		values = values[1:]
		print(values)
		with open(path+filename,'a',newline='') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(values)

def delete_order(order):
	sem.acquire()
	for previous_price in buy_orders.keys():
		for b_order in buy_orders[previous_price]["orders"]:
			if b_order.order_id == order.order_id:
				if b_order.traded_quantity > 0:
					print("cannot delete order : already traded")
					sem.release()
					return -1
				else:
					print("deletion successful")
					buy_orders[b_order.order_price]["orders"].remove(b_order)
					buy_orders[b_order.order_price]["total"]-= b_order.order_quantity
					buy_orders[b_order.order_price]["disclosed"]-= b_order.Disclosed_Quantity
					#order.delete()
					sem.release()
					return 1
	for previous_price in sell_orders.keys():
		for s_order in sell_orders[previous_price]:
			if s_order.order_id == order.order_id:
				if s_order.traded_quantity > 0:
					print("cannot delete order : already traded")
					sem.release()
					return -1
				else:
					sell_orders[s_order.order_price]["orders"].remove(s_order)
					sell_orders[s_order.order_price]["total"] -= s_order.order_quantity
					sell_orders[s_order.order_price]["dislosed"] -= s_order.Disclosed_Quantity
					#order.delete()
					print("Delete Successful")
					sem.release()
					return 1
	for m_order in market_orders["orders"]:
		if m_order.order_id == order.order_id:
			if m_order.traded_quantity > 0:
				print('Cannot Delete order Already traded')
				sem.release()
				return -1
			else:
				market_orders["orders"].remove(m_order)
				#order.delete()
				print("deleted successfully")
				sem.release()
				return 1
	for m_order in market_orders["wait-orders"]:
		if m_order.order_id == order.order_id:
			if m_order.traded_quantity > 0:
				print('Cannot Delete order Already traded')
				sem.release()
				return -1
			else:
				market_orders["wait-orders"].remove(m_order)
				print("deleted successfully")
				#order.delete()
				sem.release()
				return 1
	print("Order already executed cannot delete")
	sem.release()
	return -1


	
def update_order(order):
	k = delete_order(order)
	if k == -1:
		print('Order cannot be updated')
		return -1
	else:
		add_order(order)
		print(order.order_price)
		order.save()
def add_in_wait(order):
	sem.acquire()
	market_orders['wait-orders'].append(order)
	sem.release()
#run as a thread in parallel of the util thread
def activate_util():
	while True:
		time.sleep(5)
		sem.acquire()
		if len(market_orders['wait-orders']) > 0:
			print('Activating MR order')
			market_orders['orders'].append(market_orders['wait-orders'][0])
			del market_orders['wait-orders'][0]
			print('Activated')
		

		




