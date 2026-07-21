from django.urls import path
from django.contrib.auth.models import User
from .views import ProfileView, createAccountView, verifyEmailInfoView

urlpatterns = [
    path("my-profile/", ProfileView, name="myProfile"),
    path("members/sign-up/", createAccountView, name="signup"),
    path("members/verify_email/", verifyEmailInfoView, name="verify-email")
]
