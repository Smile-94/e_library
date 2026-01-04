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
        return f"{self.user.first_name} {self.user.last_name}"

    def __repr__(self):
        return f"<UserSubscription: {self.user.first_name} {self.user.last_name}, {self.subscription.name}, {self.pk}>"


# <<-----------------------------*** User Subscription Books ***------------------------------>>
class UserSubscriptionBooks(BaseModel):
    user_subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name="user_subscription_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="user_subscription_books")
    read_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)

    class Meta:
        db_table = "user_subscription_books"
        verbose_name = "User Subscription Books"
        verbose_name_plural = "User Subscription Books"

    def __str__(self):
        return f"{self.user_subscription.user.first_name} {self.user_subscription.user.last_name}"

    def __repr__(self):
        return f"<UserSubscriptionBooks: {self.user_subscription.user.first_name} {self.user_subscription.user.last_name}, {self.book.title}, {self.pk}>"
