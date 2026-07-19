from django.urls import path
from .views import *
from .utils import resellerPage


urlpatterns = [
     path("all-products/", allProductView, name="allProducts"),
    path("product-detail/<int:id>/",singleProductView, name="productDetails"),
    path("add-category/", addCategory, name = "add-category" ),
    path("add-product/", addProduct, name="add-products"),
    path("category/", browseProducts_inCategory, name="browse-products"),

    # RESELLER PAGE
    path("reseller/", resellerPage, name="reseller")
]
