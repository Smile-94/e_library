import json
import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from apps.book.models.book_model import Book
from apps.order.function.promotional_discount import (
    get_discounted_physical_price,
    get_product_promotional_discount,
)
from apps.order.models.cart_model import Cart, CartProduct

logger = logging.getLogger(__name__)


# <<------------------------------------*** Add To Cart View ***------------------------------------>>
class AddToCartView(LoginRequiredMixin, View):
    login_url = "account:login"  # your login URL

    def handle_no_permission(self):
        return JsonResponse({"status": "unauthenticated", "redirect_url": reverse(self.login_url)}, status=401)

    def post(self, request):
        try:
            product_id = request.POST.get("product_id")
            quantity = int(request.POST.get("quantity", 1))

            # Check if product exists
            product = Book.objects.filter(id=product_id).first()
            if not product:
                return JsonResponse({"status": "error", "message": "Book not found"}, status=404)

            if not product.has_physical_copy:
                return JsonResponse({"status": "error", "message": "This book is only for read or download"}, status=404)

            # Get or create active cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

            # Check if product already in cart
            cart_product = CartProduct.objects.filter(cart=cart, product=product).first()

            with transaction.atomic():
                if cart_product:
                    # Update quantity if product already in cart
                    cart_product.quantity += quantity
                    cart_product.price = product.physical_price
                    cart_product.discount = get_product_promotional_discount(product.id)
                    cart_product.final_price = get_discounted_physical_price(product.id)
                    cart_product.save(update_fields=["quantity", "price", "discount", "final_price"])
                else:
                    # Add new product to cart
                    new_cart_product = CartProduct.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity,
                        price=product.physical_price,
                        discount=get_product_promotional_discount(product.id),
                    )
                    new_cart_product.final_price = get_discounted_physical_price(product.id)
                    new_cart_product.save(update_fields=["final_price"])

                # Update cart totals
                cart.total_price = sum(p.price * p.quantity for p in cart.cart_products_cart.all())
                cart.total_discount = sum(
                    (i.price * i.quantity) * (i.discount / Decimal("100"))  # discount as percentage
                    for i in cart.cart_products_cart.all()
                ) or Decimal("0.00")
                cart.net_amount = cart.total_price - cart.total_discount
                cart.save(update_fields=["total_price", "total_discount", "net_amount"])

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Book added to cart",
                    "cart_count": cart.cart_products_cart.count(),
                    "cart_total": cart.net_amount,
                }
            )

        except Exception as e:
            logger.exception(f"ERROR: AddToCartView: {e}")
            return JsonResponse({"status": "error", "message": "Something went wrong"}, status=500)


# <<------------------------------------*** Cart Detail View ***------------------------------------>>
class CartDetailView(LoginRequiredMixin, View):
    login_url = "account:login"
    template_name = "cart_detail.html"
    model_class = Cart

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return redirect("account:login")

            cart = self.model_class.objects.filter(user=request.user, is_active=True).prefetch_related("cart_products_cart").first()

            context = {
                "title": "My Cart",
                "cart": cart,
                "cart_items": cart.cart_products_cart.all() if cart else [],
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "subscription": False,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Cart Detail View: {e}")
            messages.error(request, "Unable to load cart!")
            return HttpResponse("Something went wrong!")


# <<------------------------------------*** Cart Management View ***------------------------------------>>
class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                item = CartProduct.objects.get(id=data["item_id"], cart__user=request.user)

                item.quantity = int(data["quantity"])
                item.save()

                cart = item.cart
                cart.total_price = sum((i.final_price * i.quantity) for i in cart.cart_products_cart.all()) or Decimal("0.00")
                # Calculate total discount in amount
                cart.total_discount = sum(
                    (i.price * i.quantity) * (i.discount / Decimal("100"))  # discount as percentage
                    for i in cart.cart_products_cart.all()
                ) or Decimal("0.00")
                cart.net_amount = cart.total_price - cart.total_discount
                cart.save()

                return JsonResponse(
                    {
                        "success": True,
                        "item_total": item.get_subtotal(),
                        "cart_total": f"{cart.total_price:.2f}",
                        "cart_discount": f"{cart.total_discount:.2f}",
                        "cart_net_amount": f"{cart.net_amount:.2f}",
                        "cart_count": cart.cart_products_cart.count(),
                    }
                )
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Cart Update View: {e}")
            return JsonResponse({"success": False})


# <<------------------------------------*** Cart Remove Item View ***------------------------------------>>
class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            with transaction.atomic():
                data = json.loads(request.body)
                item = CartProduct.objects.get(id=data["item_id"], cart__user=request.user)
                item.delete()

                cart = item.cart
                cart.total_price = sum((i.final_price * i.quantity) for i in cart.cart_products_cart.all()) or Decimal("0.00")
                # Calculate total discount in amount
                cart.total_discount = sum(
                    (i.price * i.quantity) * (i.discount / Decimal("100"))  # discount as percentage
                    for i in cart.cart_products_cart.all()
                ) or Decimal("0.00")
                cart.net_amount = cart.total_price - cart.total_discount
                cart.save()

                return JsonResponse(
                    {
                        "success": True,
                        "cart_total": f"{cart.total_price:.2f}",
                        "cart_discount": f"{cart.total_discount:.2f}",
                        "cart_net_amount": f"{cart.net_amount:.2f}",
                        "cart_count": cart.cart_products_cart.count(),
                    }
                )
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Cart Remove View: {e}")
            return JsonResponse({"success": False})
