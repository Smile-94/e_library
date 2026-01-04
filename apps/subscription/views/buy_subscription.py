import logging
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from pysslcmz.payment import SSLCSession

from apps.common.models import ActiveStatusChoices
from apps.subscription.models.subscription_model import Subscription
from apps.subscription.models.user_subscription_model import (
    UserSubscription,
    UserSubscriptionPaymentStatus,
)

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** Buy Subscription View ***------------------------------------>>
class BuySubscriptionView(LoginRequiredMixin, View):
    model_class = UserSubscription
    subscription_model = Subscription
    login_url = "account:login"

    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = self.subscription_model.objects.filter(pk=pk).first()
            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("home:home_subscription")

            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to buy subscription!")
                return redirect("account:login")

            # # Check if user already used FREE subscription
            # if subscription.subscription_price == 0:  # Free subscription
            #     if self.model_class.objects.filter(user=request.user, subscription__subscription_price=0).exists():
            #         messages.warning(request, "You can only use free subscription once. Upgrade to a paid plan!")
            #         return redirect("home:home_subscription")

            # Optional: prevent multiple active subscriptions
            if UserSubscription.objects.filter(
                user=request.user, active_status=ActiveStatusChoices.ACTIVE.value, subscription__subscription_price__gt=0
            ).exists():
                messages.warning(request, "You already have an active subscription.")
                return redirect("home:home_subscription")

            user_subscription = UserSubscription.objects.create(
                user=request.user,
                subscription=subscription,
                payment_status=UserSubscriptionPaymentStatus.UNPAID.value,
                active_status=ActiveStatusChoices.INACTIVE.value,
            )

            # If free subscription, activate immediately
            if subscription.subscription_price == 0:
                user_subscription.active_status = ActiveStatusChoices.ACTIVE.value
                user_subscription.payment_status = UserSubscriptionPaymentStatus.PAID.value
                user_subscription.save()
                messages.success(request, "Free subscription started successfully!")
                return redirect("home:home_subscription")

            return redirect("subscription:initiate_payment", pk=user_subscription.id)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Buy Subscription View: {e}")
            messages.error(request, "Unable to load subscription details!")
            return redirect("home:home_subscription")


class InitiatePaymentView(LoginRequiredMixin, View):
    model_class = UserSubscription

    def get(self, request, pk):
        try:
            user_subscription = UserSubscription.objects.filter(pk=pk).first()
            if not user_subscription:
                messages.error(request, "User Subscription not found!")
                return redirect("home:home_subscription")

            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to initiate payment!")
                return redirect("account:login")

            sslc = SSLCSession(
                sslc_is_sandbox=True, sslc_store_id=settings.SSLCOMMERZ_STORE_ID, sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS
            )

            sslc.set_urls(
                success_url=request.build_absolute_uri(reverse("subscription:payment_success")),
                fail_url=request.build_absolute_uri(reverse("subscription:payment_fail")),
                cancel_url=request.build_absolute_uri(reverse("subscription:payment_fail")),
                ipn_url="",
            )

            sslc.set_product_integration(
                total_amount=user_subscription.subscription.subscription_price,
                currency="BDT",
                product_category="Subscription",
                product_name=user_subscription.subscription.name,
                num_of_item=1,
                shipping_method="NO",
                product_profile="general",
            )

            sslc.set_customer_info(
                name=request.user.get_full_name(),
                email=request.user.email,
                address1="N/A",
                city="Dhaka",
                country="Bangladesh",
                postcode="1234",
                phone=request.user.contact_no if request.user.contact_no else "+8801748463473",
            )

            sslc.set_additional_values(value_a=str(user_subscription.pk))

            response = sslc.init_payment()
            return redirect(response["GatewayPageURL"])
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Initiate Payment View: {e}")
            messages.error(request, "Unable to initiate payment!")
            return redirect("home:home_subscription")


@method_decorator(csrf_exempt, name="dispatch")
class PaymentSuccessView(View):
    def post(self, request):
        status = request.POST.get("status")

        if status != "VALID":
            return redirect("subscription:payment_fail")

        user_subscription_id = request.POST.get("value_a")
        user_subscription = UserSubscription.objects.filter(id=user_subscription_id).first()

        duration = user_subscription.subscription.subscription_duration_days

        user_subscription.payment_status = UserSubscriptionPaymentStatus.PAID.value
        user_subscription.active_status = ActiveStatusChoices.ACTIVE.value
        user_subscription.start_at = now()
        user_subscription.end_at = now() + timedelta(days=duration)
        user_subscription.save()

        messages.success(request, "Subscription Started successfully!")
        return redirect("home:home")


@method_decorator(csrf_exempt, name="dispatch")
class PaymentFailView(View):
    def post(self, request):
        user_subscription_id = request.POST.get("value_a")  # e.g. SUB_15

        if user_subscription_id:
            try:
                user_subscription = UserSubscription.objects.get(id=user_subscription_id)

                user_subscription.payment_status = UserSubscriptionPaymentStatus.FAILED.value
                user_subscription.active_status = ActiveStatusChoices.INACTIVE.value
                user_subscription.save()

            except UserSubscription.DoesNotExist:
                pass

        messages.error(request, "Payment failed or was cancelled. Please try again.")

        return redirect("home:home_subscription")
