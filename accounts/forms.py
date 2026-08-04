from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import BusinessProfile

class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "First Name"
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Last Name"
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username"
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password"
        })
    )

    class Meta:

        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

# ==============================
# Businessprfile FORMS
# ==============================
class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            "business_name",
            "logo",
            "website",
            "business_email",
            "phone",
            "industry",
            "description",
        ]
        
        widgets = {

            "business_name": forms.TextInput(attrs={
                "placeholder": "WorkflowRefer Ltd"
            }),

            "website": forms.URLInput(attrs={
                "placeholder": "https://yourbusiness.com"
            }),

            "business_email": forms.EmailInput(attrs={
                "placeholder": "support@company.com"
            }),

            "phone": forms.TextInput(attrs={
                "placeholder": "+234..."
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "Tell customers about your business..."
            }),

        }