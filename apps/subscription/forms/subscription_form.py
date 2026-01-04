from django import forms

from apps.subscription.models.subscription_model import Subscription


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
