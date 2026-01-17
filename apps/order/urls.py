from django.urls import path

from apps.order.views.cart_management import (
    AddToCartView,
    CartDetailView,
    RemoveCartItemView,
    UpdateCartItemView,
)

app_name = "order"

urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart-detail/", CartDetailView.as_view(), name="cart_detail"),
    path("cart/update/", UpdateCartItemView.as_view(), name="cart_update"),
    path("cart/remove/", RemoveCartItemView.as_view(), name="cart_remove"),
]
