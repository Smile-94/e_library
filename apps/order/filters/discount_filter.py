# filters.py
from django import forms
from django.db.models import Q

import django_filters

from apps.order.models.discount_model import PromotionalDiscount


# <<------------------------------------*** Promotional Discount Filter ***------------------------------------>>
class PromotionalDiscountSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by promotion_title"}),
    )

    class Meta:
        model = PromotionalDiscount
        fields = []  # individual fields optional since we are using a single search

    def filter_all_fields(self, queryset, name, value):
        """
        Filter queryset by promotion_title
        """
        return queryset.filter(promotion_title__icontains=value)
