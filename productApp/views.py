from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *

# Create your views here.
# HOME PAGE LOAD
def homePageView(request):
    products = Product.objects.all().order_by("?")
    categories = Category.objects.filter(prod__isnull=False).distinct().order_by("?").prefetch_related("prod")[:3]
    print("CATEGORIESSSSSS", categories)
    return render(
        request, 
        template_name='index.html',
        context= {
            'categories':categories,
            'products': products[:10]
            }
    )

# FOR VIEW ALL PRODUCT PAGE
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
        template_name= "productApp/all_product.html",
        context= {
            "products": products,
            "categories": categories,
            "current_category":category_param or "All Product"
        }
    )

# FOR CHECKING MORE INFO FOR A PARTICULAR SINGLE PRODUCT WHEN CLICKED
def singleProductView(request, id):
    product = get_object_or_404(Product, id = id)
    return render(
        request,
        template_name= "productApp/single_product.html",
        context= {
            "product_detail": product
        }
)

# FOR ADDING NEW PRODUCT CATEGORY
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
            template_name= "productApp/category_form.html",
            context= {
                "form": form
            }
        )

# FOR ADDING NEW PRODUCT TO PRODUCTS DB 
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
            template_name="productApp/product_form.html",
            context= {
                "form":form
            }
        )

def browseProducts_inCategory(request):
    category_name_param = request.GET.get("category_name")
    category  = get_object_or_404(Category, name=category_name_param)
    products_in_category = category.prod.all()
    return render(
        request,
        template_name="productApp/products_in_category.html",
        context={
            'category':category,
            "products_in_category":products_in_category
        }
    )