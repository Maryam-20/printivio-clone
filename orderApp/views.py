from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from productApp.models import Product
from .models import DesignFile
from django.http import JsonResponse

# Create your views here.
def designRequestOptions(request, product_title):
    product = get_object_or_404(Product, title=product_title)
    if request.method == "POST":
        # file = request.FILES
        # print(file)
        uploaded_file = request.FILES.get("design_file")
        if not uploaded_file:
            return JsonResponse({"success": False, "error": "Please select a file to upload."}, status=400)
        design_obj, created = DesignFile.objects.update_or_create(
            user=request.user,
            product = product,
            defaults= {"design_file": uploaded_file}
        )
        return JsonResponse({
        "success": True,
        "file_name": uploaded_file.name,
        # "cart_url": reverse("view-cart"),
    })
    else:
        return render(
            request,
            template_name="orderApp/design_request.html",
            context= {
                "product":product
            }
        )
