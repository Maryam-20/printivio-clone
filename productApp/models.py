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
    image = models.ImageField( upload_to= "product_image/", null=True, blank=True)
    description = models.TextField()
    material = models.CharField(max_length=100)
    finishing = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default = 0)
    status = models.CharField(max_length=50, choices = STATUS_CHOICES, default= "IN_STOCK")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)


    def __str__(self):
        return self.title

