from django.db import models
from accounts.models import BusinessProfile 
from django.utils import timezone
import uuid

# Create your models here.

class Campaign(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("ended", "Ended"),
    ]
    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name="campaigns"
    )
    
    referral_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    reward = models.CharField(
        max_length=200,
        help_text="Example: ₦5,000 Cash or 10% Discount"
    )
    referral_goal = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def referral_count(self):
        return self.referrals.count()

    @property
    def progress_percentage(self):

        if self.referral_goal == 0:
            return 0

        percentage = int(
            (self.referral_count / self.referral_goal) * 100
        )

        return min(percentage, 100)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        if not self.referral_code:
            self.referral_code = f"WR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)


class Referral(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rewarded", "Rewarded"),
    ]

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name="referrals",
    )
    referrer_name = models.CharField(
        max_length=150
    )
    referrer_email = models.EmailField()
    customer_name = models.CharField(
        max_length=150
    )
    customer_email = models.EmailField()
    customer_phone = models.CharField(
        max_length=20,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    rewarded_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.customer_name} referred by {self.referrer_name}"
    
# =========================
# Notifications
# =========================
class Notification(models.Model):

    TYPE_CHOICES = [
        ("referral", "Referral"),
        ("reward", "Reward"),
        ("campaign", "Campaign"),
        ("system", "System"),
    ]

    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=150)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="system"
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
