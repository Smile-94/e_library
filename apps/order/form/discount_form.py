from django import forms
from django.utils import timezone

from apps.order.models.discount_model import PromotionalDiscount


class PromotionalDiscountForm(forms.ModelForm):
    class Meta:
        model = PromotionalDiscount
        fields = (
            "promotion_title",
            "discount_amount",
            "discount_category",
            "discount_book",
            "active_status",
            "priority",
            "start_date",
            "end_date",
        )
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date must be greater than start date.")

        return cleaned_data
