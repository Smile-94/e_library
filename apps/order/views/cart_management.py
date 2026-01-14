from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.order.models.cart_model import Cart, CartProduct
from apps.book.models.book_model import Book
import logging
from apps.order.function.promotional_discount import get_product_promotional_discount, get_discounted_physical_price

logger = logging.getLogger(__name__)


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
                    cart_product.final_price = max(cart_product.price - cart_product.discount, 0)
                    cart_product.save(update_fields=["quantity", "price", "discount", "final_price"])
                else:
                    # Add new product to cart
                    CartProduct.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity,
                        price=product.physical_price,
                        discount=get_product_promotional_discount(product.id),
                        final_price=max(product.physical_price - get_discounted_physical_price(product.id), 0),
                    )

                # Update cart totals
                cart.total_price = sum(p.price * p.quantity for p in cart.cart_products.all())
                cart.total_discount = sum(p.discount * p.quantity for p in cart.cart_products.all())
                cart.save(update_fields=["total_price", "total_discount"])

            return JsonResponse({"status": "success", "message": "Book added to cart"})

        except Exception as e:
            logger.exception(f"ERROR: AddToCartView: {e}")
            return JsonResponse({"status": "error", "message": "Something went wrong"}, status=500)
