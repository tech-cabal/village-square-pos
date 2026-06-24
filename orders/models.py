from django.db import models
from django.contrib.auth.models import User
from inventory.models import FoodItem, Protein
import uuid

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.date.strftime('%Y-%m-%d %H:%M')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity}x {self.food.name if self.food else 'Unknown Food'}"

class OrderItemExtra(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='extras', on_delete=models.CASCADE)
    protein = models.ForeignKey(Protein, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.quantity}x {self.protein.name if self.protein else 'Unknown Protein'}"
