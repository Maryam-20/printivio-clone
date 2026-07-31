from django.contrib import admin
from .models import Category, Product, ProductQuantityOrderOptions

# Register your models here.
admin.site.register([Category, Product, ProductQuantityOrderOptions])
