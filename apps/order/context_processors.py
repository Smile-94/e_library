from apps.order.models.cart_model import Cart


def cart_summary(request):
    """
    Provides cart item count and total price
    for header display (global).
    """

    # Guest user
    if not request.user.is_authenticated:
        return {
            "cart_count": 0,
            "cart_total": 0,
        }

    cart = Cart.objects.filter(user=request.user, is_active=True).prefetch_related("cart_products_cart").first()

    if not cart:
        return {
            "cart_count": 0,
            "cart_total": 0,
        }

    return {
        "cart_count": cart.cart_products_cart.count(),
        "cart_total": cart.total_price,
    }
