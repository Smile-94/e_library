from django import forms
from django.utils.timezone import now

from apps.order.models.discount_model import PromotionalDiscount


# <<------------------------------------*** Promotional Discount Form ***------------------------------------>>
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
            "start_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # REQUIRED so Django accepts datetime-local format
        self.fields["start_date"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_date"].input_formats = ("%Y-%m-%dT%H:%M",)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        now_time = now()

        # Only apply start_date check for creation (new object)
        if not self.instance.pk and start_date and start_date < now_time:
            self.add_error("start_date", "Start date cannot be in the past.Give current date and time.")

        # End date must always be after start date
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "End date must be greater than start date.")

        return cleaned_data
