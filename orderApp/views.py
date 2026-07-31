from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from productApp.models import Product
from .models import DesignFile, Cart, CartItems
from django.http import JsonResponse
import os
from django_ratelimit.decorators import ratelimit
from decimal import Decimal

# Create your views here.

# Submit Design sample for the order
@ratelimit(key='ip', rate='5/h', block=True)
def designRequestOptions(request, product_title):
    product = get_object_or_404(Product, title=product_title)
    uploaded_file = request.FILES.get("design_file")

    if request.method == "POST":
        if not uploaded_file:
            return JsonResponse({"success": False, "error": "Please select a file to upload."}, status=400)

        ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.psd', '.ai']
        MAX_FILE_SIZE = 2 * 1024 * 1024

        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return JsonResponse({
                "success": False,
                "error": f"Unsupported file type '{ext}'. Allowed: PNG, JPEG, PSD, AI."
            }, status=400)

        if uploaded_file.size > MAX_FILE_SIZE:
            return JsonResponse({
                "success": False,
                "error": "File is too large. Maximum size is 2MB."
            }, status=400)

        if request.user.is_authenticated:
            DesignFile.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={"design_file": uploaded_file}
            )
        else:
            if not request.session.session_key:
                request.session.create()

            DesignFile.objects.update_or_create(
                session_key=request.session.session_key,
                product=product,
                user=None,
                defaults={"design_file": uploaded_file}
            )

        return JsonResponse({
            "success": True,
            "file_name": uploaded_file.name,
            "cart_url": reverse("add-to-cart", args=[product.id]),
        })

    return render(
        request,
        template_name="orderApp/design_request.html",
        context={"product": product}
    )

# PROCEED TO CART
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    posted_quantity = request.POST.get("quantity")
    if posted_quantity:
        selected_quantity = int(posted_quantity)
    else:
        first_tier = product.quantity_options.first()
        selected_quantity = first_tier.quantity_per_order if first_tier else 1
    print(selected_quantity)
    if request.user.is_authenticated:
        db_cart, created = Cart.objects.get_or_create(user=request.user)
        db_cart_items, created = CartItems.objects.get_or_create(cart=db_cart, product=product, defaults={"quantity":selected_quantity})
        if not created:
            db_cart_items.quantity += selected_quantity
            db_cart_items.save()
        
    else:
        product_id = str(product_id)
        session_cart = request.session.get("cart", {})
        if product_id in session_cart:
            session_cart[product_id] += selected_quantity
        else:
            session_cart[product_id] = selected_quantity
        request.session["cart"] = session_cart 
    return redirect("view-cart")

# VIEW ITEMS IN CART
def view_cart(request):
    suggested_products = Product.objects.all().order_by("?")
    cart_in_session = request.session.get("cart", {})
    cart_items = []
    if request.user.is_authenticated:
        if cart_in_session:
            db_cart, created = Cart.objects.get_or_create(user=request.user)
            for product_id, qty in cart_in_session.items():
                product = get_object_or_404(Product, id=product_id)
                db_cart_items, created = CartItems.objects.get_or_create(cart=db_cart, product=product, defaults={"quantity":qty})
                if not created:
                    db_cart_items.quantity +=qty
                    db_cart_items.save()
            request.session["cart"] = {}
            request.session.modified = True

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_objects = cart.items.all()
        for item_obj in item_objects:
            price = item_obj.product.price_moq
            item = {
                "product":item_obj.product,
                "quantity":item_obj.quantity,
                "price": price
            }
            cart_items.append(item)
    else:
        for product_id, qty in cart_in_session.items():
            product = get_object_or_404(Product, id=product_id)
            
            price = product.price_moq
            item ={
                "product":product,
                "quantity" : qty,
                "price":price

            }
            cart_items.append(item)
    return render(
        request, 
        template_name="orderApp/cart.html",
        context = {
            "cart_items":cart_items,
            "suggested_products":suggested_products[:5]
        }
    )

# LOGIC TO CALCULATE PRICE AS THE SELECTED QUANTITY OPTIONS CHANGES
def calculate_price(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.GET.get("quantity", 0))
    print(f"QUANTITY: {product_id} {quantity}")
    
    if product.price_per_unit and quantity > 0:
        base_total = product.price_per_unit * quantity
        five_percent_value = base_total * Decimal('0.05')
        total_price = base_total - five_percent_value
    else:
        total_price = Decimal('0.00')

    return JsonResponse({"calculated_price": f"{total_price:.2f}"})


# LOGIC TO CHECKOUT- TRANSFER CART ITEMS TO ORDER TABLE
def checkout(request):
    pass

