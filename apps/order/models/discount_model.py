from django.db import models
from django.utils import timezone

from apps.book.models.book_model import Category, Book

from apps.common.models import BaseModel, ActiveStatusChoices


# <<------------------------------------*** Discount Model ***------------------------------------>>
class PromotionalDiscount(BaseModel):
    promotion_title = models.CharField(max_length=255, null=True, blank=True)
    discount_amount = models.DecimalField(default=0, max_digits=19, decimal_places=4, null=True, blank=True)
    discount_category = models.ManyToManyField(Category, related_name="discount_category", blank=True)
    discount_book = models.ManyToManyField(Book, related_name="discount_product", blank=True)
    active_status = models.CharField(
        max_length=20, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE, null=True, blank=True
    )
    priority = models.PositiveIntegerField(default=0, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "promotional_discount_rule"
        ordering = ["-id"]
        verbose_name = "Promotional Discount"
        verbose_name_plural = "Promotional Discounts"

    def __str__(self):
        return self.promotion_title

    def __repr__(self):
        return f"<PromotionalDiscount(id={self.id}, promotion_title={self.promotion_title})>"
