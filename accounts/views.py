from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import BusinessProfile
from .forms import BusinessProfileForm

def Register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            
            # Save the user
            user = form.save()

             # Send welcome email
            send_mail(
                subject="Welcome to WorkflowRefer!",
                message=f"""
Hi {user.first_name},

Welcome to WorkflowRefer!

Your account has been created successfully.

We're excited to help you grow your business through referrals.

The WorkflowRefer Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
            messages.success(request, "Account created successfully!")

            return redirect("login") 
    else:
            
            form = RegisterForm()

    context = {
        "form": form
    }

    return render(request, "accounts/register.html", context)

def Login_user(request):
    
    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, f"Welcome back, {user.first_name}!")
            profile = BusinessProfile.objects.filter(
                user=user
            ).first()

            if not profile:
                return redirect("business_profile")

            if not profile.business_name:
                return redirect("business_profile")

            return redirect("dashboard")

        else:

            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")

@login_required
def Logout_user(request):

    logout(request)

    messages.success(request, "You have been logged out successfully.")

    return redirect("login")

# ==============================
# Businessprofile Views
# ==============================

@login_required
def Business_profile(request):

    profile, created = BusinessProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = BusinessProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Business profile updated successfully!"
            )

            return redirect("dashboard")

    else:

        form = BusinessProfileForm(request.POST, request.FILES, instance=profile)

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/business_profile.html",
        context
    )

# ==============================
# DASHBOARD VIEWS
# ==============================

@login_required
def dashboard(request):

    return render(
        request,
        "dashboard/dashboard.html"
    )
