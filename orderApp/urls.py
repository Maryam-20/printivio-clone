from django.urls import path
from .views import designRequestOptions




urlpatterns = [
    path("<str:product_title>/design_options/", designRequestOptions, name="design-request")
]
