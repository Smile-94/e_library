from django.db import models

from apps.common.models import ActiveStatusChoices, BaseModel


# <<-----------------------------*** Subscription Book Read Limit Choices ***------------------------------>>
class SubscriptionReadLimitChoices(models.TextChoices):
    LIMITED = "Limited", "Limited"
    UNLIMITED = "Unlimited", "Unlimited"


# <<-----------------------------*** Subscription Book Download Limit Choices ***------------------------------>>
class SubscriptionDownloadChoices(models.TextChoices):
    LIMITED = "Limited", "Limited"
    UNLIMITED = "Unlimited", "Unlimited"


# <<------------------------------------*** Subscription Model ***------------------------------------>>
class Subscription(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    subscription_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    subscription_duration_days = models.IntegerField(default=7)
    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE)
    book_read_limit = models.CharField(
        max_length=100, choices=SubscriptionReadLimitChoices.choices, default=SubscriptionReadLimitChoices.LIMITED
    )
    max_book_read_limit = models.IntegerField(default=0)
    book_download_limit = models.CharField(
        max_length=100, choices=SubscriptionDownloadChoices.choices, default=SubscriptionDownloadChoices.LIMITED
    )
    max_book_download_limit = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "subscription"
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Subscription: {self.name}, {self.pk}>"
