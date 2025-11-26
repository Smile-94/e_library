# filters.py
from django import forms
from django.db.models import Q

import django_filters

from apps.account.models import User
from apps.account.models.choices import GenderChoices


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name="username",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
    )
    email = django_filters.CharFilter(
        field_name="email", lookup_expr="icontains", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    contact_no = django_filters.CharFilter(
        field_name="contact_no",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact No"}),
    )
    gender = django_filters.ChoiceFilter(choices=GenderChoices)
    role = django_filters.CharFilter(field_name="role__name", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ["username", "email", "role", "contact_no", "gender"]


class UserSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by username, email, contact_no, gender"}),
    )

    class Meta:
        model = User
        fields = []  # individual fields optional since we are using a single search

    def filter_all_fields(self, queryset, name, value):
        """
        Filter queryset by username, email, contact_no, role__name, gender
        """
        return queryset.filter(
            Q(username__icontains=value)
            | Q(email__icontains=value)
            | Q(contact_no__icontains=value)
            | Q(role__name__icontains=value)
            | Q(gender__icontains=value)
        )
