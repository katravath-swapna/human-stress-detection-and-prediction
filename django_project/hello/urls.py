from django.contrib import admin
from django.urls import path
from . import views  # Import all views from the hello app

urlpatterns = [
    
    path('', views.signup, name='hello'),  # Root URL for home
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dataentry/', views.dataentry, name='dataentry'),
    path('result/', views.result, name='result'),    
]
