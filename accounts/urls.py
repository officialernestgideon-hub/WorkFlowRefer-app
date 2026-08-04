from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.Register, name='register'),
    path("login/", views.Login_user, name='login'),
    path("logout/", views.Logout_user, name='logout'),
    path("business_profile/", views.Business_profile, name='business_profile'),
   
]

