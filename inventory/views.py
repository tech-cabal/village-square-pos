from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FoodItem, Protein

@login_required
def food_menu(request):
    foods = FoodItem.objects.all()
    proteins = Protein.objects.all()
    context = {
        'foods': foods,
        'proteins': proteins,
    }
    return render(request, 'inventory/menu.html', context)

@login_required
def inventory_manage(request):
    if not request.user.is_superuser and not request.user.groups.filter(name='Admin').exists():
        return redirect('dashboard')
    
    foods = FoodItem.objects.all()
    proteins = Protein.objects.all()

    if request.method == 'POST':
        item_type = request.POST.get('type')
        item_id = request.POST.get('id')
        new_quantity = request.POST.get('quantity')
        
        if item_type == 'food':
            food = FoodItem.objects.get(id=item_id)
            food.quantity = new_quantity
            food.save()
        elif item_type == 'protein':
            protein = Protein.objects.get(id=item_id)
            protein.quantity = new_quantity
            protein.save()
            
        return redirect('inventory_manage')

    context = {
        'foods': foods,
        'proteins': proteins,
    }
    return render(request, 'inventory/manage.html', context)
