from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class AccountTypeChoices(models.TextChoices):
    BUYER = "buyer", "Buyer"
    RESELLER = "reseller", "Reseller"
    SELLER = "seller", "Seller"



class AccountType(models.Model):
    account_type = models.CharField(max_length=15, choices=AccountTypeChoices.choices, default="buyer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_type

class UserProfile(models.Model):
    contact_method = [
        ("email", "EMAIL"),
        ("phone", "PHONE"),
        ("sms", "SMS")

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, related_name="user")
    profile_image = models.ImageField(upload_to="profile_image/", null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    alternative_phone_number = models.CharField(max_length=11, null=True, blank=True)
    shipping_address = models.CharField(max_length=100, null=True, blank=True)
    accountType = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name="account", null=True, blank=True)
    account_approved = models.BooleanField(default=False)
    business_name = models.CharField(max_length=150, null=True, blank=True)
    referral_code = models.CharField(max_length=5, null=True, blank=True)
    referral_by = models.CharField(max_length=150, null=True, blank=True)
    preferred_contact_method = models.CharField(max_length=10, choices=contact_method, null=True, blank=True)
    email_verified  = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return " ".join([self.user.first_name, " ", self.user.last_name])
    
    @receiver(post_save, sender = User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile.objects.create(user = instance)
            account_type, _ = AccountType.objects.get_or_create(account_type = AccountTypeChoices.BUYER)
            profile.accountType = account_type

class StaffChoices(models.TextChoices):
    MANAGING_DIRECTOR = "managing_director", "Managing Director"
    ORDER_MANAGER = "order_manager", "Order Manager"
    STOCK_MANAGER = "stock_manager", "Stock Manager"
    LOGISTIC_MANAGER = "logistic_manager", "Logistic Manager"
    CATALOG_MANAGER = "catalog_manager", "catalog_manager"
    SALES_MANAGER = "sales_manager", "sales_manager"


class Staff(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    staff_type = models.CharField(max_length=20, choices=StaffChoices.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return " ".join([self.staff_type, "--", self.profile.user.first_name, " ", self.profile.user.last_name])



