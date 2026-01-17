from django import forms

from apps.order.models.order_model import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "address",
        "city",
        "country",
        "phone",
    ]

    class Meta:
        model = ShippingAddress
        fields = [
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "country",
            "zip_code",
            "phone",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": field.label,
                }
            )

            if name in self.REQUIRED_FIELDS:
                field.required = True
