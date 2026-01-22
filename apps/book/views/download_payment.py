import logging
from django.contrib import messages
from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from pysslcmz.payment import SSLCSession
from apps.subscription.models.user_subscription_model import UserSubscriptionBooks, UserSubscriptionPaymentStatus
from apps.common.models import ActiveStatusChoices
from apps.subscription.utils import get_active_subscription
from apps.subscription.models.user_subscription_model import BookPayment, BookPaymentStatus

logger = logging.getLogger(__name__)


# <<------------------------------------*** Book Download Payment Initiate View ***------------------------------------>>
class InitiateBookPaymentView(LoginRequiredMixin, View):
    """
    Initiates payment for a paid book.
    """

    login_url = "account:login"

    def get(self, request, sub_book_id):
        try:
            subscription = get_active_subscription(request.user)
            if not subscription:
                messages.error(request, "No active subscription found")
                return redirect("home:my_subscription_book_list")

            print(f"INFO:-------------->> Subscription: {subscription}")

            sub_book = UserSubscriptionBooks.objects.filter(user_subscription=subscription, id=sub_book_id).first()
            if not sub_book:
                return redirect("home:my_subscription_book_list")

            book = sub_book.book
            user = request.user

            # If already paid, redirect to download
            if sub_book.is_paid:
                return redirect("book:book_download", book.id)

            # Create SSLCOMMERZ session
            sslc = SSLCSession(
                sslc_is_sandbox=True, sslc_store_id=settings.SSLCOMMERZ_STORE_ID, sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS
            )

            sslc.set_urls(
                success_url=request.build_absolute_uri(reverse("book:book_payment_success")),
                fail_url=request.build_absolute_uri(reverse("book:book_payment_fail")),
                cancel_url=request.build_absolute_uri(reverse("book:book_payment_cancel")),
                ipn_url="",
            )

            sslc.set_product_integration(
                total_amount=book.digital_price,
                currency="BDT",
                product_category="Book",
                product_name=book.title,
                num_of_item=1,
                shipping_method="NO",
                product_profile="general",
            )

            sslc.set_customer_info(
                name=user.get_full_name(),
                email=user.email,
                address1="N/A",
                city="Dhaka",
                country="Bangladesh",
                postcode="1234",
                phone=user.contact_no if hasattr(user, "contact_no") else "+8801748463473",
            )

            sslc.set_additional_values(value_a=str(sub_book.id))

            response = sslc.init_payment()
            return redirect(response["GatewayPageURL"])

        except Exception as e:
            logger.exception(f"ERROR: InitiateBookPaymentView: {e}")
            return redirect("home:my_subscription_book_list")


# <<------------------------------------*** Book Download Payment Success View ***------------------------------------>>
@method_decorator(csrf_exempt, name="dispatch")
class BookPaymentSuccessView(View):
    """
    Called by SSLCOMMERZ after successful payment for a book.
    Marks the book as paid so it can be downloaded.
    """

    def post(self, request):
        try:
            status = request.POST.get("status")
            if status != "VALID":
                return redirect("book:book_payment_fail")

            sub_book_id = request.POST.get("value_a")
            sub_book = UserSubscriptionBooks.objects.filter(id=sub_book_id).first()
            if not sub_book:
                return redirect("home:my_subscription_book_list")

            with transaction.atomic():
                # Mark the paid book
                sub_book.is_paid = True
                sub_book.save(update_fields=["is_paid"])

                # Create a BookPayment entry
                BookPayment.objects.create(
                    sub_book=sub_book,
                    transaction_id=request.POST.get("tran_id"),
                    amount=sub_book.book.digital_price,
                    status=BookPaymentStatus.SUCCESS.value,
                    card_type=request.POST.get("card_type"),
                    card_issuer=request.POST.get("card_issuer"),
                    card_brand=request.POST.get("card_brand"),
                    card_issuer_country=request.POST.get("card_issuer_country"),
                    raw_response=dict(request.POST),
                )

            # Redirect user to download
            return redirect("book:book_read", sub_book.book.id)

        except Exception as e:
            logger.exception(f"ERROR: BookPaymentSuccessView: {e}")
            return redirect("home:my_subscription_book_list")


# <<------------------------------------*** Book Download Payment Fail View ***------------------------------------>>
@method_decorator(csrf_exempt, name="dispatch")
class BookPaymentFailView(View):
    """
    Called when payment fails.
    Book remains unpaid, download not allowed.
    """

    def post(self, request):
        try:
            sub_book_id = request.POST.get("value_a")
            if sub_book_id:
                sub_book = UserSubscriptionBooks.objects.filter(id=sub_book_id).first()
                if sub_book:
                    # Ensure book remains unpaid
                    sub_book.is_paid = False
                    sub_book.save(update_fields=["is_paid"])

                    # Create a BookPayment entry
                    BookPayment.objects.create(
                        sub_book=sub_book,
                        transaction_id=request.POST.get("tran_id"),
                        amount=sub_book.book.digital_price,
                        status=BookPaymentStatus.FAILED.value,
                        card_type=request.POST.get("card_type"),
                        card_issuer=request.POST.get("card_issuer"),
                        card_brand=request.POST.get("card_brand"),
                        card_issuer_country=request.POST.get("card_issuer_country"),
                        raw_response=dict(request.POST),
                    )
                    return redirect("book:book_read", sub_book.book.id)

            return redirect("home:my_subscription_book_list")

        except Exception as e:
            logger.exception(f"ERROR: BookPaymentFailView: {e}")
            return redirect("home:my_subscription_book_list")


# <<------------------------------------*** Book Download Payment Cancel View ***------------------------------------>>
@method_decorator(csrf_exempt, name="dispatch")
class BookPaymentCancelView(View):
    """
    Called when user cancels payment.
    Book remains unpaid, download not allowed.
    """

    def post(self, request):
        try:
            sub_book_id = request.POST.get("value_a")
            if sub_book_id:
                sub_book = UserSubscriptionBooks.objects.filter(id=sub_book_id).first()
                if sub_book:
                    sub_book.is_paid = False
                    sub_book.save(update_fields=["is_paid"])

                    # Save payment info
                    BookPayment.objects.create(
                        sub_book=sub_book,
                        transaction_id=request.POST.get("tran_id"),
                        amount=sub_book.book.digital_price,
                        status=BookPaymentStatus.CANCELLED.value,  # Cancelled is treated as failed
                        card_type=request.POST.get("card_type"),
                        card_issuer=request.POST.get("card_issuer"),
                        card_brand=request.POST.get("card_brand"),
                        card_issuer_country=request.POST.get("card_issuer_country"),
                        raw_response=dict(request.POST),
                    )
                    return redirect("book:book_read", sub_book.book.id)

            return redirect("home:my_subscription_book_list")

        except Exception as e:
            logger.exception(f"ERROR: BookPaymentCancelView: {e}")
            return redirect("home:my_subscription_book_list")
