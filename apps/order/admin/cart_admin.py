from apps.order.models.cart_model import Cart, CartProduct
from django.contrib import admin


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price", "total_discount", "is_active", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("is_active", "created_at", "updated_at")
    ordering = ("-id",)
    list_per_page = 10


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "price", "discount", "final_price", "added_at")
    search_fields = ("cart__user__username", "cart__user__email", "product__title")
    list_filter = ("quantity", "added_at")
    ordering = ("-id",)
    list_per_page = 10
