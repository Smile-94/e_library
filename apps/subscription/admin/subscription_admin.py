from django.contrib import admin

from apps.subscription.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subscription_price", "subscription_duration_days", "active_status")
    list_filter = ("active_status", "book_read_limit", "book_download_limit")
    search_fields = ("id", "name")
    ordering = ("-id",)
    list_per_page = 50
