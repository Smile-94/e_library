from django.db import models

from apps.account.models.user_model import User
from apps.common.models import BaseModel


# <<------------------------------------*** Author Model ***------------------------------------>>
class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "author"
        app_label = "author"

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def __repr__(self):
        return f"<Author: {self.user.username}>"


# <<------------------------------------*** Author Work Experience Model ***------------------------------------>>
class AuthorWorkExperience(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_work_experiences")
    job_title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Author Work Experience"
        verbose_name_plural = "Author Work Experiences"
        db_table = "author_work_experience"
        app_label = "author"

    def __str__(self):
        return f"{self.job_title} at {self.organization}"

    def __repr__(self):
        return f"<AuthorWorkExperience: {self.job_title} at {self.organization}>"


# <<------------------------------------*** Author Education Model ***------------------------------------>>
class AuthorEducation(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_educations")
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Author Education"
        verbose_name_plural = "Author Educations"
        db_table = "author_education"
        app_label = "author"

    def __str__(self):
        return f"{self.degree} - {self.institution}"

    def __repr__(self):
        return f"<AuthorEducation: {self.degree} - {self.institution}>"


class AuthorCertification(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_certifications")
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    issue_date = models.DateField()
    certificate_file = models.FileField(upload_to="authors/certificates/", blank=True, null=True)

    class Meta:
        verbose_name = "Author Certification"
        verbose_name_plural = "Author Certifications"
        db_table = "author_certification"
        app_label = "author"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<AuthorCertification: {self.title}, {self.issuer}, {self.issue_date}>"
