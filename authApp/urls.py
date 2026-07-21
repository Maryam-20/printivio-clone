from django.urls import path
from django.contrib.auth.models import User
from .views import ProfileView, createAccountView

urlpatterns = [
    path("my-profile/", ProfileView, name="myProfile"),
    path("members/sign-up/", createAccountView, name="signup")
]
