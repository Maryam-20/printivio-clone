from django.shortcuts import render, get_object_or_404
from .models import UserProfile

# Create your views here.
def ProfileView(request):
   profile = get_object_or_404(UserProfile, user=request.user)
   return render(
    request,
    template_name="authApp/profile.html",
    context = 
      { "profile":profile}
    
   )