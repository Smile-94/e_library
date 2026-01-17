from django.db import models

from apps.account.models.user_model import User
from apps.book.models.book_model import Book
from apps.common.models import BaseModel


class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    CONFIRMED = "confirmed", "Confirmed"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class OrderPaymentChoices(models.TextChoices):
    COD = "cod", "Cash on Delivery"
    ONLINE = "online", "Online Payment"


# <<------------------------------------*** Order Model ***------------------------------------>>
class Order(BaseModel):
    user = models.ForeignKey(User, related_name="orders_user", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    payment = models.CharField(max_length=20, choices=OrderPaymentChoices.choices, default=OrderPaymentChoices.COD)

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

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
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price - discount

    class Meta:
        db_table = "order_product"
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

    def get_subtotal(self):
        return self.final_price * self.quantity

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
