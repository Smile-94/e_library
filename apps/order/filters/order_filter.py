import django_filters
from django import forms
from django.db.models import Q

from apps.order.models.order_model import Order


# <<------------------------------------*** Order Filter ***------------------------------------>>
class OrderSearchFilter(django_filters.FilterSet):
    # Global text search
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by invoice, customer, amount",
            }
        ),
    )

    # Choice filters
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Order._meta.get_field("status").choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Order Status",
    )

    payment_method = django_filters.ChoiceFilter(
        field_name="payment",
        choices=Order._meta.get_field("payment").choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Payment Method",
    )

    payment_status = django_filters.ChoiceFilter(
        field_name="payment_status",
        choices=Order._meta.get_field("payment_status").choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Payment Status",
    )

    class Meta:
        model = Order
        fields = ["search", "status", "payment_method", "payment_status"]

    def filter_all_fields(self, queryset, name, value):
        """
        Global text search: invoice_id, customer name, net_amount
        """
        return queryset.filter(
            Q(invoice_id__icontains=value)
            | Q(user__username__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
            | Q(net_amount__icontains=value)
        )
