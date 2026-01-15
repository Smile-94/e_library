from django.urls import path
from apps.order.views.cart_management import AddToCartView

app_name = "order"

urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
]
