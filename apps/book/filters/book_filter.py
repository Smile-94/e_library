import django_filters
from django import forms
from django.db.models import Q

from apps.book.models.book_model import Book


# <<------------------------------------*** Book Filter ***------------------------------------>>
class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
    )
    author = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Author"}),
    )
    category = django_filters.CharFilter(
        field_name="category__category_name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Category"}),
    )
    isbn = django_filters.CharFilter(
        field_name="isbn",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "ISBN"}),
    )
    language = django_filters.CharFilter(
        field_name="language",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Language"}),
    )
    publication_date = django_filters.DateFilter(
        field_name="publication_date",
        lookup_expr="icontains",
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Publication Date"}),
    )
    edition = django_filters.CharFilter(
        field_name="edition",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Edition"}),
    )

    class Meta:
        model = Book
        fields = ["title", "author", "category", "isbn", "language", "publication_date", "edition"]


# <<------------------------------------*** Book Search Filter ***------------------------------------>>
class BookSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_all_fields",
        label="Search",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search by book_name, author, category, isbn, language, publication_date, edition",
            }
        ),
    )

    class Meta:
        model = Book
        fields = []  # individual fields optional since we are using a single search

    def filter_all_fields(self, queryset, name, value):
        """
        Filter queryset by book_name, author__username, category__category_name, isbn, language, publication_date, edition
        """
        return queryset.filter(
            Q(title__icontains=value)
            | Q(author__username__icontains=value)
            | Q(category__category_name__icontains=value)
            | Q(isbn__icontains=value)
            | Q(language__icontains=value)
            | Q(publication_date__icontains=value)
            | Q(edition__icontains=value)
        )
