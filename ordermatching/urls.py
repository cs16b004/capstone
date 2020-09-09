from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path("signin/", views.signinView, name="signin"),
    path('trade/',views.tradeView,name='trade'),
    path("signup/", views.signupView, name="signup_url")
    path('accepted/', views.accepted, name = 'accepted-list')
]
