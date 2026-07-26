from django.db import models
from django.contrib.auth.models import User
from productApp.models import Product

# Create your models here.
class DesignFile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="design_file")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="design_file")
    design_file = models.FileField(upload_to="design_files/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.design_file.name if self.design_file else f"Design for {self.user.get_full_name()}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}, {self.updated_at}"


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    
class OrderChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    PROCESSING = "processing", "Processing"
    READY_FOR_DELIVERY = "ready_for_delivery", "ready_for_delivery"
    DELIVERED = "delivered", "Delivered"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="order")
    status = models.CharField(max_length=20, choices=OrderChoices.choices, default="pending")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}, {self.created_at}"

    
class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_per_order_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2)

    def subtotal(self):
        return self.price_per_order_quantity * self.quantity