from django.contrib import admin
from .models import UserProfile, Staff, AccountType

# Register your models here.
admin.site.register([UserProfile, Staff, AccountType])
