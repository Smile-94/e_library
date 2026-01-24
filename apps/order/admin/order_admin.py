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
    list_display = (
        "id",
        "invoice_id",
        "user",
        "user__id",
        "total_price",
        "total_discount",
        "shipping_charge",
        "net_amount",
        "status",
        "payment",
    )
    list_filter = ("status", "payment")
    search_fields = ("user__username", "user__email", "invoice_id")
    ordering = ("-id",)
    list_per_page = 20


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "order__id",
        "product",
        "product__id",
        "quantity",
        "price",
        "discount",
        "final_price",
        "profit_amount",
    )
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "order__id", "first_name", "last_name", "address", "city", "state", "country", "zip_code", "phone")
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------*** Order Payment Admin ***------------------------------------>>
@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "order__id", "amount", "status", "payment_method")
    list_filter = ("order__status", "order__payment")
    search_fields = ("order__user__username", "order__user__email")
    ordering = ("-id",)
    list_per_page = 20
