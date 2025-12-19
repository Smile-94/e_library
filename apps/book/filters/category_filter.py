# filters.py
import django_filters
from django import forms
from django.db.models import Q

from apps.book.models.category_model import Category, SubCategory
from apps.common.models import ActiveStatusChoices


# <<------------------------------------*** Category Filter ***------------------------------------>>
class CategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(
        field_name="category_name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"}),
    )
    active_status = django_filters.ChoiceFilter(choices=ActiveStatusChoices)

    class Meta:
        model = Category
        fields = ["category_name", "active_status"]


# <<------------------------------------*** SubCategory Filter ***------------------------------------>>
class SubCategoryFilter(django_filters.FilterSet):
    sub_category_name = django_filters.CharFilter(
        field_name="sub_category_name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Sub Category Name"}),
    )
    active_status = django_filters.ChoiceFilter(choices=ActiveStatusChoices)

    class Meta:
        model = SubCategory
        fields = ["sub_category_name", "active_status"]


# <<------------------------------------*** Category Search Filter ***------------------------------------>>
class CategorySearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by category_name, active_status"}),
    )

    class Meta:
        model = Category
        fields = []  # individual fields optional since we are using a single search

    def filter_all_fields(self, queryset, name, value):
        """
        Filter queryset by category_name, active_status
        """
        return queryset.filter(Q(category_name__icontains=value) | Q(active_status__icontains=value))
