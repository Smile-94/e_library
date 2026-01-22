from django.db import models

from apps.account.models.user_model import User
from apps.book.models.book_model import Book
from apps.common.models import ActiveStatusChoices, BaseModel
from apps.subscription.models.subscription_model import Subscription


# <<-----------------------------*** User Subscription Payment Status ***------------------------------>>
class UserSubscriptionPaymentStatus(models.TextChoices):
    PAID = "paid", "Paid"
    UNPAID = "unpaid", "Unpaid"
    FAILED = "failed", "Failed"


class BookPaymentStatus(models.TextChoices):
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


# <<-----------------------------*** User Subscription Model ***------------------------------>>
class UserSubscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_subscriptions")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="user_subscriptions")
    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE)
    payment_status = models.CharField(
        max_length=10, choices=UserSubscriptionPaymentStatus.choices, default=UserSubscriptionPaymentStatus.UNPAID
    )
    start_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(null=True, blank=True)
    read_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    class Meta:
        db_table = "user_subscription"
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, Subscription: {self.subscription.name}"

    def __repr__(self):
        return f"<UserSubscription: {self.user.first_name} {self.user.last_name}, {self.subscription.name}, {self.pk}>"


# <<-----------------------------*** User Subscription Books ***------------------------------>>
class UserSubscriptionBooks(BaseModel):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name="user_subscription_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_subscription_books")
    read_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = "user_subscription_books"
        verbose_name = "User Subscription Books"
        verbose_name_plural = "User Subscription Books"

    def __str__(self):
        return f"{self.user_subscription.user.first_name} {self.user_subscription.user.last_name} - {self.book.title}"

    def __repr__(self):
        return f"<UserSubscriptionBooks: {self.user_subscription.user.first_name} {self.user_subscription.user.last_name}, {self.book.title}, {self.pk}>"


# <<-----------------------------*** Book Download Payment Model ***------------------------------>>
class BookPayment(BaseModel):
    sub_book = models.ForeignKey(UserSubscriptionBooks, on_delete=models.CASCADE, related_name="book_payment_info")
    transaction_id = models.CharField(max_length=150, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=BookPaymentStatus.choices, default=BookPaymentStatus.SUCCESS.value)
    card_type = models.CharField(max_length=20, null=True, blank=True)
    card_issuer = models.CharField(max_length=20, null=True, blank=True)
    card_brand = models.CharField(max_length=20, null=True, blank=True)
    card_issuer_country = models.CharField(max_length=20, null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "book_payment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"BookPayment #{self.pk} - Book ID: {self.sub_book.id} - Status: {self.status}"

    def __repr__(self):
        return f"<BookPayment: {self.sub_book.id}, {self.pk}, {self.status}>"
