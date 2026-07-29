from django.urls import path
from .views import designRequestOptions, add_to_cart, view_cart, calculate_price, checkout




urlpatterns = [
    path("<str:product_title>/design_options/", designRequestOptions, name="design-request"),

    path("cart/<int:product_id>/", add_to_cart, name="add-to-cart"),

    path("view-cart/", view_cart, name="view-cart"),
   path('calculate-price/<int:product_id>/', calculate_price, name='calculate_price'),
    path("checkout/", checkout, name="checkout")
]

