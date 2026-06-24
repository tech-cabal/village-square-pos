from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_menu, name='food_menu'),
    path('manage/', views.inventory_manage, name='inventory_manage'),
]
