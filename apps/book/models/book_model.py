from django.db import models

from apps.account.models.user_model import User
from apps.book.models.category_model import Category
from apps.common.models import ActiveStatusChoices, BaseModel


class BookStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PENDING = "pending", "Pending Approval"
    PUBLISHED = "published", "Published"
    REJECTED = "rejected", "Rejected"


class DownloadTypeChoices(models.TextChoices):
    FREE = "free", "Free"
    PAID = "paid", "Paid"


class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books_author")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books_category")
    book_image = models.ImageField(upload_to="books/cover/", blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    language = models.CharField(max_length=50)
    publication_date = models.DateField(blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    digital_file = models.FileField(upload_to="books/digital/", blank=True, null=True)
    preview_file = models.FileField(upload_to="books/preview/", blank=True, null=True)
    digital_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    physical_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    has_physical_copy = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=BookStatus.choices, default=BookStatus.DRAFT)
    is_read_only = models.BooleanField(default=True)
    is_downloadable = models.BooleanField(default=False)
    download_type = models.CharField(max_length=10, choices=DownloadTypeChoices.choices, default=DownloadTypeChoices.FREE.value)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="books_created_by")
    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        db_table = "book"
        app_label = "book"

    def get_book_discount(self):
        from apps.order.function.promotional_discount import (
            get_product_promotional_discount,
        )

        return get_product_promotional_discount(self.id)

    def get_discounted_price(self):
        from apps.order.function.promotional_discount import (
            get_discounted_physical_price,
        )

        return get_discounted_physical_price(self.id)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Book: {self.title}>, <pk={self.pk}>"
