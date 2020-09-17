from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home-page'),
	path("signin/", views.signinView, name="signin-page"),
	path('trade/',views.tradeView,name='trade'),
	path("signup/", views.signupView, name="signup-page"),
	path('accepted/', views.accepted, name = 'accepted-list'),
	path('waiting/', views.waiting, name = 'waiting-list'),
	path('rejected/', views.rejected, name = 'rejected-list'),
	path("ajax/getUsers",views.getUsers,name='getUsers'),
	path("logout/", views.logoutView, name="logout-page"),
	path("admin/",views.adminView,name="admin-page"),
	path("generate/",views.generateView,name="generate-page"),
]
