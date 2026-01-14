from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db.models import Q
from apps.book.models.book_model import Book
from apps.order.models.discount_model import PromotionalDiscount
from apps.common.models import ActiveStatusChoices


def get_product_promotional_discount(product_id: int) -> int:
    now = timezone.now()
    ZERO = 0  # integer zero

    product = Book.objects.select_related("category").filter(id=product_id).first()
    if not product:
        return ZERO

    promotions = (
        PromotionalDiscount.objects.filter(active_status=ActiveStatusChoices.ACTIVE, start_date__lte=now)
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=now))
        .order_by("priority")
    )

    # Product-specific promotion
    product_promo = promotions.filter(discount_book=product).first()
    if product_promo and product_promo.discount_amount is not None:
        return int(product_promo.discount_amount.quantize(Decimal("0"), rounding=ROUND_HALF_UP))

    # Category-specific promotion
    if product.category_id:
        category_promo = promotions.filter(discount_category=product.category).first()
        if category_promo and category_promo.discount_amount is not None:
            return int(category_promo.discount_amount.quantize(Decimal("0"), rounding=ROUND_HALF_UP))

    return ZERO


def get_discounted_physical_price(book_id: int) -> Decimal:
    """
    Returns discounted physical price for a book.
    Uses promotional discount percentage.
    """
    ZERO = Decimal("0.00")

    book = Book.objects.only("physical_price").filter(id=book_id).first()
    if not book:
        return ZERO

    price = book.physical_price or ZERO
    if price <= 0:
        return ZERO

    discount_percentage = get_product_promotional_discount(book_id)

    if discount_percentage <= 0:
        return price.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    discounted_price = price - (price * discount_percentage / Decimal("100"))

    # Prevent negative price
    if discounted_price < 0:
        discounted_price = ZERO

    return discounted_price.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
