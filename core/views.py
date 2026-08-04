from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Campaign
from .forms import CampaignForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import ReferralForm
from .models import Referral
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .helpers import generate_dashboard_insights
from .models import Notification
from django.db.models import Count
from django.db.models.functions import TruncMonth
import json
from django.http import JsonResponse



# Create your views here.

def Home(request):
    return render(request,"core/home.html")

@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    business = request.user.business_profile
    campaigns = Campaign.objects.filter(business=business)
    referrals = Referral.objects.filter(
        campaign__business=business
    )
    
    insights = generate_dashboard_insights(
    business,
    campaigns,
    referrals
    )
    
    recent_activity = (
    Referral.objects.filter(
        campaign__business=business
    )
    .select_related("campaign")
    .order_by("-created_at")[:5]
    )
    
    recent_rewards = (
    Referral.objects.filter(
        campaign__business=business,
        status="rewarded"
    )
    .select_related("campaign")
    .order_by("-rewarded_at")[:5]
    )
    
    top_campaigns = (
    Campaign.objects.filter(
        business=business,
        status="active"
    )
    .order_by("-created_at")[:3]
    )
    notifications = Notification.objects.filter(
    business=business
    ).order_by("-created_at")

    unread_notification_count = notifications.filter(
    is_read=False
    ).count()
    notifications = notifications[:5]
    
    context = {
        "campaign_count": campaigns.count(),
        "referral_count": referrals.count(),
        "insights": insights,
        "pending_count": referrals.filter(status="pending").count(),
        "rewarded_count": referrals.filter(status="rewarded").count(),
        "recent_activity": recent_activity,
        "recent_rewards": recent_rewards,
        "top_campaigns": top_campaigns,
        "notifications": notifications,
        "unread_notification_count": unread_notification_count,
    }
    return render(
        request,
        "dashboard/dashboard.html",
        context
    )

# =======================
# FOR CAMPAIGN
# =======================
@login_required
def campaign_list(request):

    business = request.user.business_profile
    
    campaigns = Campaign.objects.filter(
        business=business
    ).order_by("-created_at")

    return render(request,"dashboard/campaign_list.html",
        {
            "campaigns": campaigns
        },
    )
    
# =======================
# CREATE_CAMPAIGN
# =======================
@login_required
def create_campaign(request):

    business = request.user.business_profile

    if request.method == "POST":

        form = CampaignForm(request.POST)

        if form.is_valid():

            campaign = form.save(commit=False)

            campaign.business = business

            campaign.save()
            
            messages.success(
            request,
            "Campaign created successfully!"
        )

        return redirect("campaign_list")

    else:

        form = CampaignForm()

    return render(
        request,
        "dashboard/create_campaign.html",
        {
            "form": form
        }
    )
    
    # ===========================
    # EDIT Campaign
    # ===========================
    
@login_required
def edit_campaign(request, pk):

    business = request.user.business_profile

    campaign = get_object_or_404(
        Campaign,
        pk=pk,
        business=business,
    )

    if request.method == "POST":

        form = CampaignForm(
            request.POST,
            instance=campaign
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Campaign updated successfully!"
            )

            return redirect("campaign_list")

    else:

        form = CampaignForm(instance=campaign)

    return render(
        request,
        "dashboard/edit_campaign.html",
        {
            "form": form,
            "campaign": campaign,
        },
    )
    
# ===========================
# REFERAER LANDING
# ===========================
def referral_landing(request, referral_code):

    campaign = get_object_or_404(
        Campaign,
        referral_code=referral_code,
        status="active",
    )
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.campaign = campaign
            referral.save()
            
            # print("Creating notification...")
            Notification.objects.create(
                business=campaign.business,
                title="New Referral",
                message=f"{referral.referrer_name} referred {referral.customer_name}.",
                notification_type="referral",
        )
            # print("Notification ID:", notification.id)
            # print("Notification created:", Notification.id)
            
            send_mail(
                subject=f"🎉 New Referral for {campaign.title}",

                message=f"""
        Hello {campaign.business.business_name},

        A new referral has been submitted.

        Campaign:
        {campaign.title}

        Customer:
        {referral.customer_name}

        Customer Email:
        {referral.customer_email}

        Customer Phone:
        {referral.customer_phone or "Not provided"}

        Referrer:
        {referral.referrer_name}

        Referrer Email:
        {referral.referrer_email}

        Please log into WorkflowRefer to review this referral.

        Thank you,

        WorkflowRefer Team
        """,

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    campaign.business.user.email
                ],

                fail_silently=False,
            )
            return redirect(
                "referral_success"
            )
    else:
        form = ReferralForm()
        
    return render(
        request,
        "referrals/referral_landing.html",
        {
            "campaign": campaign,
            "form": form,
        },
    )

def referral_success(request):

    return render(
        request,
        "referrals/referral_success.html",
    )
    
@login_required
def campaign_detail(request, pk):

    business = request.user.business_profile

    campaign = get_object_or_404(
        Campaign,
        pk=pk,
        business=business,
    )

    return render(
        request,
        "dashboard/campaign_detail.html",
        {
            "campaign": campaign,
        },
    )
    
from .models import Referral

@login_required
def referral_list(request):

    business = request.user.business_profile

    referrals = Referral.objects.filter(
        campaign__business=business
    ).select_related(
        "campaign"
    ).order_by("-created_at")
    
     # Search
    search = request.GET.get("search")

    if search:
        referrals = referrals.filter(
            Q(customer_name__icontains=search) |
            Q(customer_email__icontains=search) |
            Q(referrer_name__icontains=search) |
            Q(referrer_email__icontains=search) |
            Q(campaign__title__icontains=search)
        )

    # Status Filter
    status = request.GET.get("status")
    if status:
        referrals = referrals.filter(status=status)
        
    context = {
        "referrals": referrals,
        "search": search,
        "status": status,
    }

    return render(
        request,
        "dashboard/referral_list.html",
        context,
    )
    
@login_required
def referral_detail(request, pk):

    business = request.user.business_profile

    referral = get_object_or_404(
        Referral,
        pk=pk,
        campaign__business=business,
    )

    return render(
        request,
        "dashboard/referral_detail.html",
        {
            "referral": referral,
        },
    )
    
    # ===============================
    # APPROVE Referral
    # ===============================
@login_required
def approve_referral(request, pk):

    business = request.user.business_profile

    referral = get_object_or_404(
        Referral,
        pk=pk,
        campaign__business=business,
    )

    if referral.status == "pending":

        referral.status = "approved"
        referral.save()

        messages.success(
            request,
            "Referral approved successfully."
        )

    return redirect(
        "referral_detail",
        pk=referral.pk
    )
    
    # ===================================
    # REWARD REFERRER          
    # ===================================
@login_required
def reward_referral(request, pk):

    business = request.user.business_profile

    referral = get_object_or_404(
        Referral,
        pk=pk,
        campaign__business=business,
    )

    if referral.status == "approved":

        referral.status = "rewarded"
        referral.save()

        messages.success(
            request,
            "Referral marked as rewarded."
        )

    return redirect(
        "referral_detail",
        pk=referral.pk
    )
    
# ===============================
# REWARD TRACKING
# ===============================
@login_required
def reward_list(request):

    business = request.user.business_profile

    rewards = Referral.objects.filter(
        campaign__business=business,
        status="rewarded"
    ).select_related("campaign").order_by("-created_at")

    context = {

        "rewards": rewards,

        "reward_count": rewards.count(),

    }

    return render(
        request,
        "dashboard/reward_list.html",
        context,
    )
    
# MARK AS READ
@login_required
def mark_notification_read(request, pk):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    business = request.user.business_profile

    notification = get_object_or_404(
        Notification,
        pk=pk,
        business=business
    )

    notification.is_read = True
    notification.save()

    return JsonResponse({
        "success": True
    })

@login_required
def mark_all_notifications_read(request):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    business = request.user.business_profile

    Notification.objects.filter(
        business=business,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({
        "success": True
    })

@login_required
def notification_list(request):

    business = request.user.business_profile

    notifications = Notification.objects.filter(
        business=business
    )

    return render(
        request,
        "dashboard/notifications.html",
        {
            "notifications": notifications,
        },
    )
    
    
# ANALYTICS
@login_required
def analytics_dashboard(request):

    business = request.user.business_profile

    campaigns = Campaign.objects.filter(
        business=business
    )

    referrals = Referral.objects.filter(
        campaign__business=business
    )
    
    monthly_referrals = (
    referrals
    .annotate(month=TruncMonth("created_at"))
    .values("month")
    .annotate(total=Count("id"))
    .order_by("month")
    )

    growth_labels = [
        item["month"].strftime("%b")
        for item in monthly_referrals
    ]

    growth_data = [
        item["total"]
        for item in monthly_referrals
    ]
    
    top_campaign = campaigns.order_by("-created_at").first()

    if top_campaign:
        top_campaign_progress = top_campaign.progress_percentage
    else:
        top_campaign_progress = 0
    campaign_performance = campaigns.order_by("-created_at")[:5]

    context = {

        "campaign_count": campaigns.count(),

        "referral_count": referrals.count(),

        "approved_count": referrals.filter(
            status="approved"
        ).count(),

        "rewarded_count": referrals.filter(
            status="rewarded"
        ).count(),

        "pending_count": referrals.filter(
            status="pending"
        ).count(),

        "campaigns": campaigns,
        "growth_labels": json.dumps(growth_labels),
        "growth_data": json.dumps(growth_data),
        
        "top_campaign": top_campaign,
        "top_campaign_progress": top_campaign_progress,
        "campaign_performance": campaign_performance,

    }

    return render(
        request,
        "dashboard/analytics.html",
        context
    )
    
# clear notification
@login_required
def clear_notifications(request):

    if request.method != "POST":
        return JsonResponse(
            {"success": False},
            status=405
        )

    business = request.user.business_profile

    Notification.objects.filter(
        business=business
    ).delete()

    return JsonResponse({

        "success": True

    })