from django import forms

from apps.subscription.models.subscription_model import Subscription
from apps.subscription.models.user_subscription_model import UserSubscription


# <<------------------------------------*** Subscription Form ***------------------------------------>>
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subscription Name"}),
        #     "subscription_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Subscription Price"}),
        #     "subscription_duration_days": forms.NumberInput(
        #         attrs={"class": "form-control", "placeholder": "Subscription Duration Days"}
        #     ),
        #     "book_read_limit": forms.Select(attrs={"class": "form-control", "placeholder": "Book Read Limit"}),
        #     "book_download_limit": forms.Select(attrs={"class": "form-control", "placeholder": "Book Download Limit"}),
        # }


# <<------------------------------------*** User Subscription Form ***------------------------------------>>
class UserSubscriptionForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",  # HTML5 input type for datetime
                "class": "form-control",
            }
        ),
        required=False,
    )

    end_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}), required=False)

    class Meta:
        model = UserSubscription
        fields = "__all__"
