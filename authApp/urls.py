from django.urls import path
from django.contrib.auth.models import User
from .views import ProfileView

urlpatterns = [
    path("my-profile/", ProfileView, name="myProfile")
]
