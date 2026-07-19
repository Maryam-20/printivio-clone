from django.shortcuts import render, redirect

def resellerPage(request):
    return render(
        request,
        template_name="reseller.html"
    )