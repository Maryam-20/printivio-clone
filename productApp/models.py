from django.db import models
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length= 50, null=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    STATUS_CHOICES = [
        ("IN_STOCK", "In stock"),
        ("OUT_OF_STOCK", "Out of stock")
    ]

    title = models.CharField(max_length= 100)
    image = models.ImageField(upload_to="product_image/", null=True, blank=True)
    description = models.TextField()
    material = models.CharField(max_length=100)
    finishing = models.CharField(max_length=100)
    quantity_in_stock = models.PositiveIntegerField(default = 0)
    minimum_quantity_per_order = models.PositiveBigIntegerField(default=0)
    price_moq = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, default= "IN_STOCK")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="prod")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.minimum_quantity_per_order and self.price_per_unit:

            base_total = self.minimum_quantity_per_order * self.price_per_unit

            five_percent_discount = base_total * Decimal("0.05")

            self.price_moq = base_total - five_percent_discount
        else:
            self.price_moq = Decimal("0.00")

        super().save(*args, **kwargs)


class ProductQuantityOrderOptions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="quantity_options")
    quantity_per_order = models.PositiveIntegerField()

    class Meta:
        ordering = ["quantity_per_order"]
        unique_together = ("product", "quantity_per_order")


    def __str__(self):
        return f"{self.product.title} - {self.quantity_per_order} units"

