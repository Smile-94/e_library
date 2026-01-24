from django.contrib import admin

from apps.order.models.cart_model import Cart, CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user__id", "total_price", "total_discount", "is_active", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("is_active", "created_at", "updated_at")
    ordering = ("-id",)
    list_per_page = 10


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "cart__id", "product", "product__id", "quantity", "price", "discount", "final_price", "added_at")
    search_fields = ("cart__user__username", "cart__user__email", "product__title")
    list_filter = ("quantity", "added_at")
    ordering = ("-id",)
    list_per_page = 10
