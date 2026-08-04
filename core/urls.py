from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name='home'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("campaign_list/", views.campaign_list, name="campaign_list"),
    path("campaign/create/", views.create_campaign, name="create_campaign"),
    path("campaign/<int:pk>/edit/",views.edit_campaign,name="edit_campaign"),
    path("r/<str:referral_code>/",views.referral_landing,name="referral_landing",),
    path("campaign/<int:pk>/", views.campaign_detail,name="campaign_detail",),
    path("success/",views.referral_success,name="referral_success",),
    path("dashboard/referrals/",views.referral_list,name="referral_list",),
    path("dashboard/referrals/<int:pk>/",views.referral_detail,name="referral_detail",),
    path("dashboard/referrals/<int:pk>/approve/",views.approve_referral,name="approve_referral",),
    path("dashboard/referrals/<int:pk>/reward/",views.reward_referral,name="reward_referral",),
    path("dashboard/rewards/",views.reward_list,name="reward_list",),
    path("notifications/<int:pk>/read/",views.mark_notification_read,name="mark_notification_read",),
    path("notifications/read-all/",views.mark_all_notifications_read,name="mark_all_notifications_read",),
    path("notifications/",views.notification_list,name="notification_list",),
    path("dashboard/analytics/",views.analytics_dashboard,name="analytics",),
    path("notifications/clear/",views.clear_notifications,name="clear_notifications",),
]
