from django.contrib import admin
from apps.order.models.discount_model import PromotionalDiscount


# <<----------------------------------- Promotional Discount Admin ---------------------------------------->>
@admin.register(PromotionalDiscount)
class PromotionalDiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "promotion_title", "discount_amount", "active_status", "priority", "start_date", "end_date")
    search_fields = ("id", "promotion_title")
    ordering = ("-id",)
    list_filter = ("active_status", "start_date", "end_date")
    list_per_page = 20
