from django.shortcuts import render
from .models import Order
from .forms  import OrderForm
import openpyxl
import json
from django.http import HttpResponse, JsonResponse
from .consumers import Generator
from .ordermatching import add_order, start_matcher
import threading
# Create your views here.
def order(request):
    if request.method == "POST":
    #   Here get
    #   Retrieve User id from session for now I am using using the id as 'YAUID(Yet another user id)'
    #        
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        print(request.POST.keys())
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        keys = request.POST.keys()
        userid              = 'YAID' #change this to one received from session
        if request.session['username']:
            userid = request.session['username']
        quantity            = int(request.POST["order_quantity"])      
        o_type              = request.POST["order_type"]         
        o_cat               = request.POST["order_category"]
        #noextra            = (True, False)[request.POST["extra"] == "Yes"]
        price               = -1
        all_or_none         = False                 #Default if not specified
        Minimum_fill        = 0                     #Default if not specified
        dis_quant           = quantity              #Default if not specified
        traded_quantity     = 0
       
        if "order_price" in keys and request.POST["order_price"] != '' :
            price           = round(float(request.POST["order_price"]),2)
        if "all_or_none" in keys:
            all_or_none     = (False, True)[request.POST["all_or_none"] == "on"]
        
        if "Minimum_fill" in keys and request.POST['Minimum_fill'] != '' :
            Minimum_fill    = int(request.POST['Minimum_fill'])
        
        if "Disclosed_Quantity" in keys and request.POST["Disclosed_Quantity"] != '' :
            dis_quant       = int(request.POST["Disclosed_Quantity"])
        error_msg = ''
        if all_or_none:
            Minimum_fill = quantity
            dis_quant = quantity
        else:
            if Minimum_fill > quantity:
                error_msg = 'Minimum fill is greater than order quantity'
            if Minimum_fill > dis_quant:
                error_msg += ' and Minimum fill is greater than disclosed quantity'
            if dis_quant > quantity:
                error_msg += ' and Disclosed Quantity is greater than order quantity'
        if error_msg != '':
            form = OrderForm()
            my_orders = Order.objects.all().filter(user_id = request.session['username'])
            return render(request,'order/order.html',{'form': form, 'my_orders': my_orders, 'error_msg': error_msg})
        order = Order.objects.create(order_price       = price,\
                                    order_category     = o_cat,\
                                    order_type         = o_type,\
                                    order_quantity     = quantity,\
                                    All_or_none        = all_or_none,\
                                    Minimum_fill       = Minimum_fill,\
                                    Disclosed_Quantity = dis_quant,\
                                    user_id            = userid,\
                                    order_status       = 'Waiting',\
                                    traded_quantity    = traded_quantity)
                                    
        order.save()
        add_order(order)
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        print(order.All_or_none)
        print(order.Minimum_fill)
        print(order.Disclosed_Quantity)
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        #k = order.save()
            #print(k)
        form = OrderForm()
        my_orders = Order.objects.all().filter(user_id = request.session['username'])
        success_msg = 'Order placed successfully'
        return render(request,'order/order.html',{'order':order, 'form': form, 'my_orders': my_orders, 'success_msg': success_msg})
    else:
        form = OrderForm()
        my_orders = Order.objects.all().filter(user_id = request.session['username'])
        return render(request, 'order/order.html', {'form': form, 'my_orders': my_orders})
def startgenerate(request):
    if request.method == "POST":
        # g = Generator()
        start_matcher()
        return render(request, 'order/gen-success.html')
    else:
        return render(request, 'order/generator.html')

def room(request):
    return render(request, 'order/room.html')

def room_test(request):
    return render(request, 'order/test.html')

def startmatcher(request):
    print('started startmatcher')
    #start_matcher()
    return render(request, 'order/room.html')