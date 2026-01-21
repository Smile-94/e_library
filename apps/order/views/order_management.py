import logging
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from pysslcmz.payment import SSLCSession

from apps.order.form.shipping_address_form import ShippingAddressForm
from apps.order.models.cart_model import Cart
from apps.order.models.order_model import (
    Order,
    OrderPayment,
    OrderPaymentMethodChoices,
    OrderPaymentStatusChoices,
    OrderProduct,
    OrderStatusChoices,
)

logger = logging.getLogger(__name__)

SHIPPING_CHARGE = Decimal("50.00")


class CheckoutView(LoginRequiredMixin, View):
    login_url = "account:login"
    template_name = "checkout.html"

    def get(self, request):
        try:
            cart = Cart.objects.filter(user=request.user, is_active=True).prefetch_related("cart_products_cart__product").first()

            if not cart or cart.cart_products_cart.count() == 0:
                messages.warning(request, "Your cart is empty.")
                return redirect("order:cart_detail")

            context = {
                "title": "Checkout",
                "cart": cart,
                "cart_items": cart.cart_products_cart.all(),
                "shipping_charge": SHIPPING_CHARGE,
                "grand_total": cart.net_amount + SHIPPING_CHARGE,
                "payment_methods": OrderPaymentMethodChoices.choices,
                "shipping_form": ShippingAddressForm(),
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            messages.error(request, "Unable to load checkout page!")
            logger.exception(f"ERROR:------>> Error occurred in Checkout View: {e}")
            return redirect("home:home")


class PlaceOrderView(LoginRequiredMixin, View):
    login_url = "account:login"

    def post(self, request):
        try:
            cart = Cart.objects.filter(user=request.user, is_active=True).first()
            if not cart or cart.cart_products_cart.count() == 0:
                messages.error(request, "Cart is empty.")
                return redirect("order:checkout")

            shipping_form = ShippingAddressForm(request.POST)
            payment_method = request.POST.get("payment_method")

            if not shipping_form.is_valid():
                messages.error(request, "Invalid shipping information.")
                return redirect("order:checkout")

            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_price=cart.total_price,
                    total_discount=cart.total_discount,
                    shipping_charge=SHIPPING_CHARGE,
                    net_amount=cart.net_amount + SHIPPING_CHARGE,
                    payment=payment_method,
                    payment_status=OrderPaymentStatusChoices.PENDING,
                    status=OrderStatusChoices.PENDING,
                )

                # Order items
                for item in cart.cart_products_cart.all():
                    OrderProduct.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.price,
                        discount=item.discount,
                        final_price=item.final_price,
                    )

                # Shipping
                shipping = shipping_form.save(commit=False)
                shipping.order = order
                shipping.save()

                # Payment record
                OrderPayment.objects.create(
                    order=order,
                    amount=order.net_amount,
                    status="pending",
                    payment_method=payment_method,
                )

                # Deactivate cart
                cart.is_active = False
                cart.save(update_fields=["is_active"])

            # COD → done
            if payment_method == OrderPaymentMethodChoices.COD:
                order.payment_status = OrderPaymentStatusChoices.CONFIRMED
                order.status = OrderStatusChoices.PENDING
                order.save(update_fields=["payment_status", "status"])

                messages.success(request, "Order placed successfully!")
                return redirect("home:home")

            # ONLINE → redirect to gateway
            return redirect("order:order_initiate_payment", pk=order.pk)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Place Order View: {e}")
            messages.error(request, "Unable to place order!")
            return redirect("home:home")


# <<------------------------------------*** Order Initiate Payment View ***------------------------------------>>
class OrderInitiatePaymentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        order = Order.objects.filter(pk=pk, user=request.user).first()
        if not order:
            messages.error(request, "Order not found.")
            return redirect("cart:detail")

        sslc = SSLCSession(
            sslc_is_sandbox=True,
            sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
            sslc_store_pass=settings.SSLCOMMERZ_STORE_PASS,
        )

        sslc.set_urls(
            success_url=request.build_absolute_uri(reverse("order:order_payment_success")),
            fail_url=request.build_absolute_uri(reverse("order:order_payment_fail")),
            cancel_url=request.build_absolute_uri(reverse("order:order_payment_fail")),
            ipn_url="",
        )

        sslc.set_product_integration(
            total_amount=float(order.net_amount),
            currency="BDT",
            product_category="Order",
            product_name=f"Order #{order.id}",
            num_of_item=order.order_placed_products.count(),
            shipping_method="YES",
            product_profile="general",
        )

        # CUSTOMER INFO
        sslc.set_customer_info(
            name=request.user.get_full_name() or "Customer",
            email=request.user.email or "customer@example.com",
            address1="N/A",
            city="Dhaka",
            country="Bangladesh",
            postcode="1234",
            phone=request.user.contact_no or "+8801000000000",
        )

        # ✅ SHIPPING INFO (THIS WAS MISSING)
        shipping = order.order_shipping_address
        sslc.set_shipping_info(
            shipping_to=request.user.get_full_name(),
            address=shipping.address,
            city=shipping.city,
            postcode=shipping.zip_code,
            country=shipping.country,
        )

        sslc.set_additional_values(value_a=str(order.pk))

        response = sslc.init_payment()
        logger.info(f"SSLCOMMERZ RESPONSE: {response}")

        if response.get("status") == "SUCCESS" and response.get("GatewayPageURL"):
            return redirect(response["GatewayPageURL"])

        messages.error(
            request,
            response.get("failedreason", "Unable to initiate payment."),
        )
        return redirect("cart:detail")


# <<------------------------------------*** Order Payment Success View ***------------------------------------>>
@method_decorator(csrf_exempt, name="dispatch")
class OrderPaymentSuccessView(View):
    def post(self, request):
        post_data = request.POST.dict()
        if request.POST.get("status") != "VALID":
            return redirect("order:payment_fail")

        order_id = request.POST.get("value_a")
        order = Order.objects.filter(pk=order_id).first()

        transaction_id = post_data.get("tran_id", None)
        amount = post_data.get("amount", 0)
        cared_type = post_data.get("card_type", "online").lower()
        card_issuer = post_data.get("card_issuer", "unknown").lower()
        card_brand = post_data.get("card_brand", "unknown").lower()
        card_issuer_country = post_data.get("card_issuer_country", "unknown").lower()

        with transaction.atomic():
            order.payment_status = OrderPaymentStatusChoices.CONFIRMED
            order.status = OrderStatusChoices.PENDING.value
            order.references_id = transaction_id
            order.save()

            order.payment_info.transaction_id = transaction_id
            order.payment_info.status = "paid"
            order.payment_info.raw_response = "online"
            order.payment_info.amount = amount
            order.payment_info.card_type = cared_type
            order.payment_info.card_issuer = card_issuer
            order.payment_info.card_brand = card_brand
            order.payment_info.card_issuer_country = card_issuer_country
            order.payment_info.raw_response = post_data
            order.payment_info.save()

        messages.success(request, "Payment successful!")
        return redirect("home:home")


# <<------------------------------------*** Order Payment Fail View ***------------------------------------>>
@method_decorator(csrf_exempt, name="dispatch")
class OrderPaymentFailView(View):
    def post(self, request):
        order_id = request.POST.get("value_a")
        order = Order.objects.filter(pk=order_id).first()

        if order:
            order.payment_status = OrderPaymentStatusChoices.FAILED
            order.status = OrderStatusChoices.PENDING.value
            order.save()

            order.payment_info.status = "failed"
            order.payment_info.raw_response = request.POST.dict()
            order.payment_info.save()

        messages.error(request, "Payment failed or cancelled.")
        return redirect("cart:detail")
