from django import forms
from .models import Campaign
from .models import Referral

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = [
            "title",
            "description",
            "reward",
            "referral_goal",
            "status",
            "start_date",
            "end_date",
        ]

        widgets = {

            "title": forms.TextInput(attrs={
                "placeholder": "Summer Referral Campaign"
            }),

            "description": forms.Textarea(attrs={
                "placeholder": "Explain how customers earn rewards..."
            }),

            "reward": forms.TextInput(attrs={
                "placeholder": "₦5,000 Cash"    
            }),

            "referral_goal": forms.NumberInput(attrs={
                "placeholder": "100"
            }),

            "start_date": forms.DateInput(attrs={
                "type": "date"
            }),

            "end_date": forms.DateInput(attrs={
                "type": "date"
            }),

        }
        
# =======================
# REFERRER LANDING FORM
# =======================
class ReferralForm(forms.ModelForm):

    class Meta:

        model = Referral

        fields = [
            "referrer_name",
            "referrer_email",
            "customer_name",
            "customer_email",
            "customer_phone",
        ]