from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

# Create your views here.

def homePageView(request):
    products = Product.objects.all()
    return render(
        request, 
        template_name='index.html',
        context= {
            'products': products[:8]
            }
    )

def allProductView(request):
    categories = Category.objects.values_list("name", flat=True).distinct().order_by("name")
    category_param = request.GET.get('category')
    if category_param and category_param.lower() != "all":
        products = Product.objects.filter(category__name = category_param)
        print(products)
    else:
        products = Product.objects.all()
    return render(
        request,
        template_name= "all_product.html",
        context= {
            "products": products,
            "categories": categories,
            "current_category":category_param or "All Product"
        }
    )
def categoryProducts(request, id):
    products = Product.objects.all().filter(id = id)
    return render(
        request,
        template_name="all_product.html",
        context= {
            "product":products
        }
    )
def singleProductView(request, id):
    product = get_object_or_404(Product, id = id)
    return render(
        request,
        template_name= "single_product.html",
        context= {
            "product_detail": product
        }
)

def addCategory(request):
    if request.method == "POST":
      form = CategoryForm(request.POST)
      if form.is_valid():
          form.save()
      return redirect("allProducts")
    
    else:
        form = CategoryForm
        return render(
            request,
            template_name= "category_form.html",
            context= {
                "form": form
            }
        )
    
def addProduct(request):
    if request.method == "POST":
      form = ProductForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
      return redirect("home")
    else:
        form = ProductForm
        return render(
            request,
            template_name="product_form.html",
            context= {
                "form":form
            }
        )