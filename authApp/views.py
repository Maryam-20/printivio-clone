from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import SignUpForm
from django.http import HttpResponse

# Create your views here.
def createAccountView(request):
   if request.method == "POST":
      form = SignUpForm(request.POST)
      if form.is_valid():
         form.save()
         return HttpResponse("Account Created Successfully!")
   else:
      form = SignUpForm()
   return render(
      request,
      template_name="authApp/signup.html",
      context= {
         "form":form
      }
      
   )


def ProfileView(request):
   profile = get_object_or_404(UserProfile, user=request.user)
   return render(
    request,
    template_name="authApp/profile.html",
    context = 
      { "profile":profile}
    
   )