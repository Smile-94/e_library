from django.contrib import admin

from apps.subscription.models import (
    BookPayment,
    UserSubscription,
    UserSubscriptionBooks,
)


# <<------------------------------------*** User Subscription Admin ***------------------------------------>>
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "user__id",
        "subscription",
        "subscription__id",
        "active_status",
        "payment_status",
        "start_at",
        "end_at",
        "read_count",
        "download_count",
    )
    list_filter = ("active_status",)
    search_fields = ("id", "user__username", "subscription__name")
    ordering = ("-id",)
    list_per_page = 50


# <<------------------------------------*** User Subscription Books Admin ***------------------------------------>>
@admin.register(UserSubscriptionBooks)
class UserSubscriptionBooksAdmin(admin.ModelAdmin):
    list_display = ("id", "user_subscription", "book", "book__id", "read_count", "download_count")
    list_filter = ("user_subscription__active_status",)
    search_fields = ("id", "user_subscription__user__username", "book__title")
    ordering = ("-id",)
    list_per_page = 50


# <<------------------------------------*** Book Payment Admin ***------------------------------------>>
@admin.register(BookPayment)
class BookPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "sub_book", "sub_book__user_subscription", "amount", "status", "created_at", "updated_at")
    list_filter = ("sub_book__user_subscription__active_status",)
    search_fields = ("id", "sub_book__user_subscription__user__username", "sub_book__book__title")
    ordering = ("-id",)
    list_per_page = 50
