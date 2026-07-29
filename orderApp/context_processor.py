from django.shortcuts import get_object_or_404
from .models import Cart


def getCartCount(request):
    if request.user.is_authenticated:

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    else:
        cart = request.session.get("cart", {})
        cart_count = len(cart)
    return {
        "cart_count": cart_count
    }