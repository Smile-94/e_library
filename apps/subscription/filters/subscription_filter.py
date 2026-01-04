import django_filters
from django import forms
from django.db.models import Q

from apps.subscription.models.subscription_model import Subscription


# <<------------------------------------*** Subscription Search Filter ***------------------------------------>>
class SubscriptionSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by subscription_name, subscription_price, subscription_duration_days, book_read_limit, book_download_limit",
            }
        ),
    )
    book_read_limit = django_filters.CharFilter(
        field_name="book_read_limit",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Book Read Limit"}),
    )
    book_download_limit = django_filters.CharFilter(
        field_name="book_download_limit",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Book Download Limit"}),
    )

    class Meta:
        model = Subscription
        fields = ["search", "book_read_limit", "book_download_limit"]

    def filter_all_fields(self, queryset, name, value):
        """
        Filter queryset by subscription_name, subscription_price, subscription_duration_days, book_read_limit, book_download_limit
        """
        return queryset.filter(
            Q(name__icontains=value) | Q(subscription_price__icontains=value) | Q(subscription_duration_days__icontains=value)
        )
