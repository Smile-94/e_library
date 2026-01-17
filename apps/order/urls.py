from django.urls import path

from apps.order.views.cart_management import (
    AddToCartView,
    CartDetailView,
    RemoveCartItemView,
    UpdateCartItemView,
)
from apps.order.views.my_order import MyOrdersView, OrderDetailView
from apps.order.views.order_management import (
    CheckoutView,
    OrderInitiatePaymentView,
    OrderPaymentFailView,
    OrderPaymentSuccessView,
    PlaceOrderView,
)

app_name = "order"

# <<------------------------------------*** Cart Management Url ***------------------------------------>>
urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart-detail/", CartDetailView.as_view(), name="cart_detail"),
    path("cart/update/", UpdateCartItemView.as_view(), name="cart_update"),
    path("cart/remove/", RemoveCartItemView.as_view(), name="cart_remove"),
]

# <<------------------------------------*** Order Management Url ***------------------------------------>>
urlpatterns += [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("place-order/", PlaceOrderView.as_view(), name="place_order"),
    path("payment/<int:pk>/", OrderInitiatePaymentView.as_view(), name="order_initiate_payment"),
    path("payment/success/", OrderPaymentSuccessView.as_view(), name="order_payment_success"),
    path("payment/fail/", OrderPaymentFailView.as_view(), name="order_payment_fail"),
]

# <<------------------------------------*** My Order Url ***------------------------------------>>
urlpatterns += [
    path("my-orders/", MyOrdersView.as_view(), name="my_orders"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="my_order_detail"),
]
