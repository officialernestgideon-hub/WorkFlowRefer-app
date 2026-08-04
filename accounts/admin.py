from django.contrib import admin
from .models import Profile, BusinessProfile

# Register your models here.

# This lets us manage profiles from the Django admin panel.
admin.site.register(BusinessProfile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "country", "created_at")
    search_fields = ("user__username", "user__email", "phone")

