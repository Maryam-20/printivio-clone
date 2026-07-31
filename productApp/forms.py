from django import forms
from .models import *

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            "name"
        ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title", "description","material", "finishing", "quantity_in_stock","minimum_quantity_per_order","price_per_unit", "category", "image"
        ]

class ProductQuantityOrderOptionsForm(forms.ModelForm):
    class Meta:
        model = ProductQuantityOrderOptions
        fields ="__all__"