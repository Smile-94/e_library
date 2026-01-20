import datetime

from django.db import models
from django.utils.crypto import get_random_string

from apps.account.models.user_model import User
from apps.book.models.book_model import Book
from apps.common.models import BaseModel
from apps.order.function.promotional_discount import get_discounted_physical_price


class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class OrderPaymentMethodChoices(models.TextChoices):
    COD = "cod", "Cash on Delivery"
    ONLINE = "online", "Online Payment"


class OrderPaymentStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    FAILED = "failed", "Failed"


# <<------------------------------------*** Order Model ***------------------------------------>>
class Order(BaseModel):
    invoice_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, related_name="orders_user", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    payment = models.CharField(max_length=20, choices=OrderPaymentMethodChoices.choices, default=OrderPaymentMethodChoices.COD.value)
    payment_status = models.CharField(
        max_length=20, choices=OrderPaymentStatusChoices.choices, default=OrderPaymentStatusChoices.PENDING
    )
    references_id = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, *args, **kwargs):
        # Auto-calculate net_amount
        if not self.net_amount:
            self.net_amount = self.total_price - self.total_discount + (self.shipping_charge or 0)

        super().save(*args, **kwargs)  # Save first to get PK

        # Generate unique invoice_id if not set
        if not self.invoice_id:
            today_str = datetime.datetime.now().strftime("%y%m%d")  # e.g., 260117
            base_invoice = f"INV{today_str}{str(self.pk).zfill(4)}"

            # Ensure uniqueness
            invoice_candidate = base_invoice
            while Order.objects.filter(invoice_id=invoice_candidate).exists():
                # append 3 random digits if collision occurs
                invoice_candidate = f"{base_invoice}{get_random_string(3, allowed_chars='0123456789')}"

            self.invoice_id = invoice_candidate
            super().save(update_fields=["invoice_id"])

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"

    def __repr__(self):
        return f"<Order: {self.user.username}, {self.pk}, {self.status}>"


# <<-----------------------------*** Order Product Model ***------------------------------>>
class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_placed_products")
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price - discount
    profit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # purchase_price - final_price

    class Meta:
        db_table = "order_product"
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

    def get_subtotal(self):
        return self.final_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.purchase_price:
            self.purchase_price = self.product.purchase_price

        if not self.profit_amount:
            self.profit_amount = self.final_price - self.purchase_price
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"

    def __repr__(self):
        return f"<OrderProduct: {self.product.title}, {self.pk}>"


class ShippingAddress(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_shipping_address")
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "shipping_address"
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<ShippingAddress: {self.first_name} {self.last_name}, {self.pk}>"


# <<------------------------------------*** Order Payment Model ***------------------------------------>>
class OrderPayment(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment_info")
    transaction_id = models.CharField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # pending / paid / failed
    payment_method = models.CharField(max_length=20)  # cod / online
    card_type = models.CharField(max_length=20, null=True, blank=True)
    card_issuer = models.CharField(max_length=20, null=True, blank=True)
    card_brand = models.CharField(max_length=20, null=True, blank=True)
    card_issuer_country = models.CharField(max_length=20, null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "order_payment"

    def __str__(self):
        return f"Payment #{self.pk} - {self.order.id}"

    def __repr__(self):
        return f"<Payment: {self.order.id}, {self.pk}>"
