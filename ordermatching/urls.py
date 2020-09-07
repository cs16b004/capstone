from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('signup/', views.signup, name = 'signup-page'),
    path('signin/', views.signin, name = 'signin-page'),
]