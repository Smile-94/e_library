from django.contrib import admin

from apps.book.models.category_model import Category


# <<------------------------------------*** Category Admin ***------------------------------------>>
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name", "category_image", "active_status", "created_at", "updated_at")
    list_filter = ("active_status",)
    search_fields = ("category_name",)
    ordering = ("-id",)


# # <<------------------------------------*** SubCategory Admin ***------------------------------------>>
# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ("category", "sub_category_name", "sub_category_image", "active_status", "created_at", "updated_at")
#     list_filter = ("active_status",)
#     search_fields = ("sub_category_name", "category__category_name")
#     ordering = ("-id",)
