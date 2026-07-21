from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import SignUpForm, UserEditForm, ProfileEditForm
from django.http import HttpResponse

# Create your views here.
def createAccountView(request):
   if request.method == "POST":
      form = SignUpForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect("verify-email")
   else:
      form = SignUpForm()
   return render(
      request,
      template_name="authApp/signup.html",
      context= {
         "form":form
      }
      
   )

def verifyEmailInfoView(request):
   return render(
      request,
      template_name="authApp/verify_email.html"
   )

def ProfileView(request):
   profile = get_object_or_404(UserProfile, user=request.user)
   return render(
    request,
    template_name="authApp/profile.html",
    context = 
      { "profile":profile}
    
   )

def editProfileView(request):
   profile = get_object_or_404(UserProfile, user=request.user)
   if request.method == "POST":
      user_form = UserEditForm(request.POST, instance=request.user)
      profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         return redirect("myProfile")
   else:
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=profile)
      return render(
         request,
         template_name="authApp/edit_profile.html",
         context= {
            "user_form":user_form,
            "profile_form":profile_form,
            "profile":profile
         }
      )