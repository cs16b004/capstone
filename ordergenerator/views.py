from django.shortcuts import render
from .models import Order, Generator
from .forms  import OrderForm
import openpyxl
# Create your views here.
def order(request):
    if request.method == "POST":
        price               = round(float(request.POST["order_price"]),2)
        quantity            = int(request.POST["order_quantity"])      
        o_type              = request.POST["order_type"]         
        o_cat               = request.POST["order_category"]
        noextra             = (False, True)[request.POST["No_extra"] == "on"]
        print('===============',noextra, price+10,quantity)
        if noextra == False:
            all_or_none      = (False, True)[request.POST.get("All_or_none",'off') == "on"]
            print("-----------------------------",request.POST.get("Disclosed_Quantity",str(quantity)))
            
            if "Disclosed_Quantity" in request.POST["Disclosed_Quantity"]:
                dis_quant    = int(request.POST["Disclosed_Quantity"])
            else:
                dis_quant    = quantity
            
            if "Minimum_Fill" in request.POST["Minimum_Fill"]:
                Minimum_Fill    = int(request.POST["Minimum_Fill"])
            else:
                Minimum_Fill    = 0
            order = Order.objects.create(order_price        = price,\
                                        order_category     = o_cat,\
                                        order_type         = o_type,\
                                        order_quantity     = quantity,\
                                        No_extra           = noextra,\
                                        All_or_none        = all_or_none,\
                                        Minimum_fill       = Minimum_fill,\
                                        Disclosed_Quantity = dis_quant,)                            
            order.save()
            print(order)
        else:
            order = Order.objects.create(order_price        = price,\
                                        order_category     = o_cat,\
                                        order_type         = o_type,\
                                        order_quantity     = quantity,\
                                        No_extra           = noextra,)
            order.save()
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
