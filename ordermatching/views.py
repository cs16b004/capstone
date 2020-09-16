from django.shortcuts import render, redirect
from ordermatching.models import UserSignup
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from ordergenerator.models import Order

def home(request):
	return render(request, 'home/home.html')

def getUsers(request):
    queryset = UserSignup.objects.all()
    return JsonResponse({'users' : list(queryset.values())})

def tradeView(request):
    username = ""
    if request.session.has_key('username'):
      username = request.session['username']
    return render(request,'trade.html',{'username' : username})

def signinView(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        pwd = request.POST['password']
        request.session['username'] = user_name
        user_obj = UserSignup.objects.filter(username = user_name, password=pwd).exists()
        if user_obj :
            print("user object exists")
            return render(request,'trade.html')
        else :
            return render(request,'signup/signup.html')
    else:
        return render(request, 'signin/signin.html')

def signupView(request):
    if request.method == "POST":
        user_name = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pwd = request.POST['password']

        request.session['username'] = user_name

        if UserSignup.objects.filter(username=user_name).exists():
            print("Username Taken") # use toolkit to show it there(js, css etc)
        else :
            user1 = UserSignup.objects.create(username = user_name,firstname=first_name,lastname=last_name,password=pwd)
            user2 = User.objects.create_user(username = user_name,first_name=first_name,last_name=last_name,password=pwd,is_staff=True,is_active=True,is_superuser=True)
            user1.save()
            user2.save()

            user = authenticate(request,username=user_name,password=pwd )
            if user :
                login(request,user)
            print("User Created")
            return render(request,'home/home.html')
    else :
        return render(request,'signup/signup.html')

def logoutView(request):
    try:
        del request.session['username']
    except:
       pass
    return render(request,'home/home.html')


def accepted(request):
	accepted_list = Order.objects.all().filter(order_status = 'Accepted')
	buy = Order.objects.all().filter(order_category = 'Buy')
	sell = Order.objects.all().filter(order_category = 'Sell')
	buy_shares = 0
	sell_shares = 0
	for order in buy:
		buy_shares += order.traded_quantity
	for order in sell:
		sell_shares += order.traded_quantity
	# print(len(accepted_list))
	return render(request, 'tradeslist/accepted/accepted.html', {'accepted_list': accepted_list, 'buy_shares': buy_shares, 'sell_shares': sell_shares})

def waiting(request):
	waiting_list = Order.objects.all().filter(order_status = 'Waiting')
	buy = Order.objects.all().filter(order_category = 'Buy')
    sell = Order.objects.all().filter(order_category = 'Sell')
    buy_shares = 0
    sell_shares = 0
    for order in buy:
        buy_shares += order.traded_quantity
    for order in sell:
        sell_shares += order.traded_quantity
	return render(request, 'tradeslist/waiting/waiting.html', {'waiting_list': waiting_list, 'buy_shares': buy_shares, 'sell_shares': sell_shares})

def rejected(request):
    rejected_list = Order.objects.all().filter(order_status = 'Rejected')
    buy = Order.objects.all().filter(order_category = 'Buy')
    sell = Order.objects.all().filter(order_category = 'Sell')
    buy_shares = 0
    sell_shares = 0
    for order in buy:
        buy_shares += order.traded_quantity
    for order in sell:
        sell_shares += order.traded_quantity
	return render(request, 'tradeslist/rejected/rejected.html', {'rejected_list': rejected_list, 'buy_shares': buy_shares, 'sell_shares': sell_shares})

def adminView(request):
	pass
