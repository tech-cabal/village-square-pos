import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'village_square.settings')
django.setup()

from django.contrib.auth.models import User, Group
from inventory.models import FoodItem, Protein

def populate():
    # Create Groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    staff_group, _ = Group.objects.get_or_create(name='Staff')

    # Create Superuser (Admin)
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin_user.groups.add(admin_group)
        print("Created superuser 'admin'")

    # Create a Staff User
    if not User.objects.filter(username='staff1').exists():
        staff_user = User.objects.create_user('staff1', 'staff1@example.com', 'staff123')
        staff_user.groups.add(staff_group)
        print("Created staff user 'staff1'")

    # Create Foods
    foods = [
        {"name": "Jollof Rice", "price": 2000, "quantity": 50, "desc": "Delicious Nigerian Jollof"},
        {"name": "Fried Rice", "price": 2200, "quantity": 40, "desc": "Special Fried Rice"},
        {"name": "Pounded Yam", "price": 2500, "quantity": 30, "desc": "Smooth Pounded Yam"},
        {"name": "Egusi Soup", "price": 2000, "quantity": 30, "desc": "Rich Egusi Soup"},
        {"name": "Amala", "price": 1800, "quantity": 45, "desc": "Hot Amala"},
        {"name": "Eba", "price": 1500, "quantity": 50, "desc": "Garri Eba"},
        {"name": "Ofada Rice", "price": 2300, "quantity": 20, "desc": "Local Ofada Rice with sauce"},
    ]
    for f in foods:
        FoodItem.objects.get_or_create(name=f['name'], defaults={'price': f['price'], 'quantity': f['quantity'], 'description': f['desc']})

    # Create Proteins
    proteins = [
        {"name": "Beef", "price": 700, "quantity": 100},
        {"name": "Fish", "price": 1500, "quantity": 50},
        {"name": "Chicken", "price": 2000, "quantity": 80},
        {"name": "Turkey", "price": 2500, "quantity": 60},
        {"name": "Goat Meat", "price": 2000, "quantity": 70},
        {"name": "Egg", "price": 500, "quantity": 120},
    ]
    for p in proteins:
        Protein.objects.get_or_create(name=p['name'], defaults={'price': p['price'], 'quantity': p['quantity']})
    
    print("Populated Foods and Proteins")

if __name__ == '__main__':
    populate()
