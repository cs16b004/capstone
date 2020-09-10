from django.shortcuts import render, redirect
from ordermatching.models import UserSignup
from django.template import loader
from django.http import HttpResponse, JsonResponse

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
            print("user object ecists")
            return render(request,'trade.html')
        else :
            return render(request,'/signup/signup.html')
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
            user1.save()
            print("User Created")
            return render(request,'home/home.html')
    else :
        return render(request,'signup/signup.html')


def accepted(request):
	return render(request, 'tradeslist/accepted/accepted.html')
