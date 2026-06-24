import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from inventory.models import FoodItem, Protein
from .models import Order, OrderItem, OrderItemExtra

@login_required
def pos_new_order(request):
    foods = FoodItem.objects.filter(quantity__gt=0)
    proteins = Protein.objects.filter(quantity__gt=0)
    
    # Pass proteins as JSON for the frontend modal
    proteins_data = [{'id': p.id, 'name': p.name, 'price': str(p.price)} for p in proteins]
    
    context = {
        'foods': foods,
        'proteins_json': json.dumps(proteins_data),
    }
    return render(request, 'orders/pos.html', context)

@login_required
def pos_submit_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_items = data.get('items', [])
            total_amount = data.get('total', 0)
            
            if not cart_items:
                return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)
            
            # Create Order
            order = Order.objects.create(
                staff=request.user,
                total_amount=total_amount
            )
            
            # Process Items
            for item in cart_items:
                food = FoodItem.objects.get(id=item['food_id'])
                qty = item['quantity']
                subtotal = item['subtotal']
                
                # Check inventory (simple check)
                if food.quantity < qty:
                    return JsonResponse({'status': 'error', 'message': f'Not enough {food.name} in stock'}, status=400)
                
                # Deduct inventory
                food.quantity -= qty
                food.save()
                
                order_item = OrderItem.objects.create(
                    order=order,
                    food=food,
                    quantity=qty,
                    subtotal=subtotal
                )
                
                # Process Extras
                for extra in item.get('extras', []):
                    protein = Protein.objects.get(id=extra['protein_id'])
                    extra_qty = extra['quantity'] * qty # Total extras needed for this food item quantity
                    
                    if protein.quantity < extra_qty:
                        return JsonResponse({'status': 'error', 'message': f'Not enough {protein.name} in stock'}, status=400)
                    
                    protein.quantity -= extra_qty
                    protein.save()
                    
                    OrderItemExtra.objects.create(
                        order_item=order_item,
                        protein=protein,
                        quantity=extra['quantity'],
                        price=protein.price
                    )
                    
            return JsonResponse({'status': 'success', 'order_id': order.id})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def order_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/receipt.html', {'order': order})
