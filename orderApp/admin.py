from django.contrib import admin
from .models import DesignFile, Cart, CartItems, Order, OrderItems

# Register your models here.
admin.site.register([DesignFile, Cart, CartItems, Order, OrderItems])