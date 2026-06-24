from django.contrib import admin
from .models import Order, OrderItem, OrderItemExtra

class OrderItemExtraInline(admin.TabularInline):
    model = OrderItemExtra
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'staff', 'total_amount', 'date')
    search_fields = ('order_number',)
    list_filter = ('date', 'staff')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'quantity', 'subtotal')
    inlines = [OrderItemExtraInline]
