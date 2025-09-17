from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/' , views.dashboard, name='dashboard'),    
    
    path('user_list/<str:id>/' , views.user_list, name='user_list'), 
    path('jeweller_list/' , views.jeweller_list, name='jeweller_list'), 
]