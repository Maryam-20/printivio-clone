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
            "title",
            "description",
            "material",
            "finishing",
            "quantity",
            "price",
            "category",
            "image"
        ]