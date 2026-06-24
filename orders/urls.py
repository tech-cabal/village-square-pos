from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.pos_new_order, name='pos_new_order'),
    path('submit/', views.pos_submit_order, name='pos_submit_order'),
    path('receipt/<int:order_id>/', views.order_receipt, name='order_receipt'),
]
