from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length = 11,
        required=True,
        label="Phone Number",
        widget=forms.TextInput(attrs={"placeholder":"Enter your phone number"})
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "first_name", "last_name", "email", "phone_number"
        ]
        labels = {
            "first_name": "Your Name",
            "last_name": "Your Surname",
            "email": "Email Address",
            "phone_number": "Phone Number",
        }
        widgets = {
            "first_name" : forms.TextInput(attrs={"placeholder": "Enter your name"}),

            "last_name": forms.TextInput(attrs={"placeholder": "Enter your surname"}),

            "email": forms.EmailInput(attrs={"placeholder": "Enter your email"})

        }
    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Password"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter password"


        self.fields["password2"].label = "Re-Type Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Re-Type Password"

    
    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        clean_phone = phone.replace(" ", "").replace("-", "")
        if not clean_phone.isdigit():
            raise forms.ValidationError("Phone number can only contain digits.")
        return clean_phone


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        phone_number = self.cleaned_data.get("phone_number")
        email = self.cleaned_data.get("email")
        user.username = email
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
            user=user,
            defaults={"phone_number": phone_number}
        )
        return user
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {
            "first_name": "Your Name",
            "last_name": "Your Surname",
            "email": "Email Address",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Enter your surname"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter your email"}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_image", "dob", "phone_number", "alternative_phone_number", "shipping_address"]
        labels = {
            "profile_image": "Profile Picture",
            "dob": "Date of Birth",
            "phone_number": "Phone Number",
            "alternative_phone_number": "Alternative Phone Number",
            "shipping_address": "Shipping Address",
        }
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Enter your phone number"}),
            "alternative_phone_number": forms.TextInput(attrs={"placeholder": "Enter an alternative number"}),
            "shipping_address": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter your shipping address"}),
        }