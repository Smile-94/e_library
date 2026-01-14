from django.db import models
from apps.book.models.book_model import Book
from apps.common.models import BaseModel
from apps.account.models.user_model import User


# <<------------------------------------*** Cart Model ***------------------------------------>>
class Cart(BaseModel):
    user = models.ForeignKey(User, related_name="cart_user", on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)  # only one active cart per user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

    def __repr__(self):
        return f"<Cart: {self.user.first_name} {self.user.last_name}, {self.pk}>"


# <<-----------------------------*** Cart Product Model ***------------------------------>>
class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_products")
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="cart_products")
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price - discount
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_product"
        verbose_name = "Cart Product"
        verbose_name_plural = "Cart Products"

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
