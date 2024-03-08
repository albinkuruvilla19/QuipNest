from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('profile_list',views.profile_list,name="profile_list"),
    path('profile/<int:pk>',views.profile,name="profile"),
    path('login/',views.loginn,name="login"),
    path('logout',views.logoutt,name="logout"),
    path('register/',views.register,name="register"),
    path('update_user',views.update_user,name="update_user"),
]