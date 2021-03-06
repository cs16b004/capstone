from django.shortcuts import render, redirect
from .models import Order
from .forms  import OrderForm
import openpyxl
import json
from django.http import HttpResponse, JsonResponse
from .consumers import Generator
from .ordermatching import add_order, start_matcher, delete_order, update_order
import threading
# Create your views here.
def order(request):
    if request.method == "POST":
    #   Here get
    #   Retrieve User id from session for now I am using using the id as 'YAUID(Yet another user id)'
    #        
        if 'delete-btn' in request.POST:
            order = Order.objects.filter(order_id = request.POST['delete-btn'])[0]
            # Ayush add your function here for deleteing
            if order.traded_quantity == 0:
                if delete_order(order) == 1:
                #del_order.delete()
                    order.delete()
                    success_msg = 'Order deleted successfully'
                    form = OrderForm()
                    my_orders = Order.objects.all().filter(user_id = request.session['username'])
                    return render(request,'order/order.html',{'form': form, 'my_orders': my_orders, 'success_msg': success_msg})
            # else:
            form = OrderForm()
            my_orders = Order.objects.all().filter(user_id = request.session['username'])
            return render(request,'order/order.html',{'form': form, 'my_orders': my_orders, 'error_msg': 'Cannot delete Order in execution'})
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        print(request.POST)
        print("-----------------------------------------------------------------")
        print("-----------------------------------------------------------------")
        keys = request.POST.keys()
        userid              = 'YAID' #change this to one received from session
        if 'username' in request.session:
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
        i = 1
        if all_or_none:
            Minimum_fill = quantity
            dis_quant = quantity
        else:
            temp = False
            if Minimum_fill > quantity:
                error_msg += '&emsp;' +str(i) +'. Minimum fill is greater than order quantity <br>'
                i += 1
                temp = True
            if Minimum_fill > dis_quant:
                error_msg += '&emsp;' +str(i) +'. Minimum fill is greater than disclosed quantity <br>'
                i += 1
                temp = True
            if dis_quant > quantity:
                error_msg += '&emsp;' +str(i) +'. Disclosed Quantity is greater than order quantity <br>'
                i += 1
                temp = True
            if temp:
                if 'modify-btn' not in request.POST:
                    error_msg = 'Order is not placed successfully because <br>' + error_msg
        if o_type == 'LM':
            if price > 0:
                check_price = price/0.05
                if not check_price.is_integer():
                    error_msg += '&emsp;' +str(i) +'. Order Price is not a multiple of 0.05 <br>'
            else:
                error_msg += '&emsp;' +str(i) +'. Limit Order Price should be greater than 0 <br>'
        else:
            print(o_cat)
            price = -1

        if 'modify-btn' in request.POST:
            print('Modify Order')
            if error_msg == '':
                
                """order = Order.objects.filter(order_id = request.POST['modify-btn']).update( order_price       = price,\
                                                                                    rorde_category     = o_cat,\
                                                                                    order_type         = o_type,\
                                                                                    order_quantity     = quantity,\
                                                                                    All_or_none        = all_or_none,\
                                                                                    Minimum_fill       = Minimum_fill,\
                                                                                    Disclosed_Quantity = dis_quant,\
                                                                                    user_id            = userid,\
                """
                order = Order.objects.filter(order_id = request.POST['modify-btn'])[0]#,traded_quantity    = traded_quantity)
                # Ayush add your function for updating
                print(o_cat)
                order.order_price        = price
                order.order_category     = o_cat
                order.order_type         = o_type
                order.order_quantity     = quantity
                order.All_or_none        = all_or_none
                order.Minimum_fill       = Minimum_fill
                order.Disclosed_Quantity = dis_quant
                order.user_id            = userid
                print(order.order_id)
                k = -1
                if order.traded_quantity == 0:
                    k = update_order(order)
                if k == 1:
                    form = OrderForm()
                    my_orders = Order.objects.all().filter(user_id = request.session['username'])
                    success_msg = 'Order Modified successfully'
                    return render(request,'order/order.html',{'form': form, 'my_orders': my_orders, 'success_msg': success_msg})
                else:
                    error_msg = 'Order in execution'
                    form = OrderForm()
                    my_orders = Order.objects.all().filter(user_id = request.session['username'])
                    error_msg = 'Order is not modified successfully because <br>' + error_msg

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
        add_order(order)
        print("added order")
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
        return render(request,'order/order.html',{'form': form, 'my_orders': my_orders, 'success_msg': success_msg})
    else:
        if 'username' in request.session:
            form = OrderForm()
            my_orders = Order.objects.all().filter(user_id = request.session['username'])
            return render(request, 'order/order.html', {'form': form, 'my_orders': my_orders})
        else:
            print('Ok')
            return redirect('signin-page')
def startgenerate(request):
    if request.method == "POST":
        g = Generator()
        #start_matcher()
        return render(request, 'order/gen-success.html')
    else:
        return render(request, 'order/generator.html')

def room(request):
    return render(request, 'order/room.html')

def room_test(request):
    return render(request, 'order/test.html')

def startmatcher(request):
    if request.method == "POST":
        start_matcher()
        return render(request, 'order/gen-success.html')
    else:
        return render(request, 'order/generator.html')
