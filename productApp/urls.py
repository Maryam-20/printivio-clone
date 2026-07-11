from django.urls import path
from .views import *


urlpatterns = [
     path("all-products/", allProductView, name="allProducts"),
    path("product-detail/<int:id>/",singleProductView, name="productDetails"),
    path("category-product/<int:id>/", categoryProducts, name = "category-products"),
    path("add-category/", addCategory, name = "add-category" ),
    path("add-product/", addProduct, name="add-products")
]
