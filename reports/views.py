from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import FoodItem, Protein
from orders.models import Order, OrderItem
from django.db.models import Sum
from django.utils import timezone

@login_required
def dashboard(request):
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_orders = Order.objects.filter(date__gte=today_start)
    total_sales = sum(order.total_amount for order in today_orders)
    order_count = today_orders.count()
    
    available_foods = FoodItem.objects.filter(quantity__gt=0).count()
    low_stock_foods = FoodItem.objects.filter(quantity__lt=10)
    low_stock_proteins = Protein.objects.filter(quantity__lt=10)

    context = {
        'total_sales': total_sales,
        'order_count': order_count,
        'available_foods': available_foods,
        'low_stock_foods': low_stock_foods,
        'low_stock_proteins': low_stock_proteins,
    }
    return render(request, 'reports/dashboard.html', context)

@login_required
def sales_report(request):
    orders = Order.objects.all().order_by('-date')
    
    # Best selling food calculation could be complex, simple version:
    food_sales = OrderItem.objects.values('food__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:5]

    context = {
        'orders': orders,
        'food_sales': food_sales,
    }
    return render(request, 'reports/sales_report.html', context)
