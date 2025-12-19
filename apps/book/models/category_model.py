from django.db import models

from apps.common.models import ActiveStatusChoices, BaseModel


class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    category_image = models.ImageField(upload_to="categories/", blank=True, null=True)
    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "category"
        app_label = "book"

    def __str__(self):
        return self.category_name

    def __repr__(self):
        return f"<Category: {self.category_name}>, <pk={self.pk}>"


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    sub_category_name = models.CharField(max_length=100, unique=True)
    sub_category_image = models.ImageField(upload_to="subcategories/", blank=True, null=True)
    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        db_table = "sub_category"
        app_label = "book"

    def __str__(self):
        return self.sub_category_name

    def __repr__(self):
        return f"<SubCategory: {self.sub_category_name}>, <pk={self.pk}>"
