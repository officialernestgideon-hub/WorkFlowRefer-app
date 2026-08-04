from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()


# ==============================
# Business Industry Choices
# ==============================

INDUSTRY_CHOICES = [
    ("technology", "Technology"),
    ("fashion", "Fashion"),
    ("food", "Food & Restaurant"),
    ("health", "Health"),
    ("education", "Education"),
    ("finance", "Finance"),
    ("real_estate", "Real Estate"),
    ("ecommerce", "E-commerce"),
    ("travel", "Travel & Tourism"),
    ("professional_services", "Professional Services"),
    ("retail", "Retail"),
    ("other", "Other"),
]

class BusinessProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="business_profile"
    )

    business_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="business_logos/", blank=True, null=True)
    website = models.URLField(blank=True)
    business_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        default="other",
    )
    logo = models.ImageField(
    upload_to="business_logos/",
    blank=True,
    null=True
    )
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name
    
    
