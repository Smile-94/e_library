from django.urls import path

from apps.subscription.views.buy_subscription import (
    BuySubscriptionView,
    InitiatePaymentView,
    PaymentFailView,
    PaymentSuccessView,
)

app_name = "subscription"

urlpatterns = [
    path("buy-subscription/<int:pk>/", BuySubscriptionView.as_view(), name="buy_subscription"),
    path("initiate-payment/<int:pk>/", InitiatePaymentView.as_view(), name="initiate_payment"),
    path("payment-success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("payment-fail/", PaymentFailView.as_view(), name="payment_fail"),
]
