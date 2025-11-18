from django.db import models


# <<------------------------------------*** Gender Choices ***------------------------------------>>
class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    UNMENTIONED = "unmentioned", "Unmentioned"
    OTHER = "other", "Other"
