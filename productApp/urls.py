from django.urls import path
from . import views as pv


urlpatterns = [
     path("all-products/", pv.allProductView, name="allProducts"),
    path("product-detail/<int:id>/", pv.singleProductView, name="productDetails")
]
