from django.shortcuts import render

def home(request):
	return render(request, 'home/home.html')

def signin(request):
	return render(request, 'signin/signin.html')

def signup(request):
	return render(request, 'signup/signup.html')
