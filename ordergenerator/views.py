from django.shortcuts import render
from .models import Order, Generator
from .forms  import OrderForm
import openpyxl
# Create your views here.
def order(request):
    if request.method == "POST":
    #   Here get
    #   Retrieve User id from session for now I am using using the id as 'YAUID(Yet another user id)'
    #        
        userid              = 'YAID' #change this to one received from session
        price               = round(float(request.POST["order_price"]),2)
        quantity            = int(request.POST["order_quantity"])      
        o_type              = request.POST["order_type"]         
        o_cat               = request.POST["order_category"]
        noextra             = (True, False)[request.POST["extra"] == "Yes"]
        #print('===============',noextra, price+10,quantity)
        if noextra == False:
            all_or_none     = (False, True)[request.POST["All_or_none"] == "Yes"]

            print("-----------------------------------------------------------------")
            print("-----------------------------------------------------------------")
            print(request.POST)
            print("-----------------------------------------------------------------")
            print("-----------------------------------------------------------------")
            #Minimum_fill    = request.POST.get('Minimum_fill',0)
            #dis_quant       = request.POST.get('Disclosed_Quantity',quantity)
            print(request.POST['Minimum_fill'])
            Minimum_fill = 0
            if request.POST['Minimum_fill']:
                Minimum_fill = int(request.POST['Minimum_fill'])
                
            dis_quant        = quantity 
            if request.POST["Disclosed_Quantity"]:
                dis_quant    = int(request.POST["Disclosed_Quantity"])
            order = Order.objects.create(order_price       = price,\
                                        order_category     = o_cat,\
                                        order_type         = o_type,\
                                        order_quantity     = quantity,\
                                        No_extra           = noextra,\
                                        All_or_none        = all_or_none,\
                                        Minimum_fill       = Minimum_fill,\
                                        Disclosed_Quantity = dis_quant,\
                                        user_id            = userid,)                            
            order.save()
            print(order)
        else:
            order = Order.objects.create(order_price       = price,\
                                        order_category     = o_cat,\
                                        order_type         = o_type,\
                                        order_quantity     = quantity,\
                                        No_extra           = noextra,\
                                        user_id            = userid)
            k = order.save()
            #print(k)
        return render(request,'order/success.html')
    else:
        form = OrderForm()
        return render(request, 'order/order.html', {'form': form})
def startgenerate(request):
    if request.method == "POST":
        g = Generator()
        return render(request, 'order/gen-success.html')
    else:
        return render(request, 'order/generator.html')
