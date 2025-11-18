from django.db import models


# <<------------------------------------*** Active Status Choices ***------------------------------------>>
class ActiveStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


# <<------------------------------------*** Base Model ***------------------------------------>>
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
