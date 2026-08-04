from django.contrib import admin
from .models import Campaign, Referral, Notification

admin.site.register(Referral)

# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "business",
        "status",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "start_date",
    )

    search_fields = (
        "title",
        "business__business_name",
    )
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "business",
        "notification_type",
        "is_read",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "is_read",
    )

    search_fields = (
        "title",
        "message",
    )
    