from django.db import models

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
    quantity_inStock = models.PositiveIntegerField(default = 0)
    quantity_per_order = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, default= "IN_STOCK")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_quantityOrder = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name="prod")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title

