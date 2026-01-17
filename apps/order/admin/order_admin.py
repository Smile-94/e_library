from django.contrib import admin

from apps.order.models.order_model import (
    Order,
    OrderPayment,
    OrderProduct,
    ShippingAddress,
)


# <<------------------------------------*** Order Admin ***------------------------------------>>
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "total_discount", "net_amount", "status", "payment")
    list_filter = ("status", "payment")
    search_fields = ("user__username", "user__email")
    ordering = ("-id",)
    list_per_page = 20


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "discount", "final_price")
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("order", "first_name", "last_name", "address", "city", "country", "zip_code", "phone")
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------*** Order Payment Admin ***------------------------------------>>
@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "status", "payment_method")
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20
