from django.contrib import admin

from apps.book.models.book_model import Book


# <<------------------------------------*** Book Admin ***------------------------------------>>
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "isbn",
        "language",
        "publication_date",
        "edition",
        "digital_file",
        "preview_file",
        "digital_price",
        "physical_price",
        "has_physical_copy",
        "status",
        "is_read_only",
        "is_downloadable",
        "created_by",
        "active_status",
    )
    list_filter = ("active_status", "status", "is_read_only", "is_downloadable")
    search_fields = (
        "title",
        "author__username",
        "category__category_name",
        "isbn",
        "language",
        "publication_date",
        "edition",
        "digital_file",
        "preview_file",
        "digital_price",
        "physical_price",
        "has_physical_copy",
        "status",
        "is_read_only",
        "is_downloadable",
        "created_by__username",
    )
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50
