from django.contrib import admin

from apps.author.models import Author, AuthorCertification, AuthorEducation, AuthorWorkExperience


# <<------------------------------------*** Author Admin ***------------------------------------>>
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "user__id", "created_at", "updated_at")
    search_fields = ("user__username", "user__email", "user__contact_no")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------*** Author Work Experience Admin ***------------------------------------>>
@admin.register(AuthorWorkExperience)
class AuthorWorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "job_title", "organization", "start_date", "end_date", "created_at", "updated_at")
    search_fields = ("author__username", "author__email", "author__contact_no")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------*** Author Education Admin ***------------------------------------>>
@admin.register(AuthorEducation)
class AuthorEducationAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "degree", "institution", "start_year", "end_year", "created_at", "updated_at")
    search_fields = ("author__username", "author__email", "author__contact_no")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------*** Author Certification Admin ***------------------------------------>>
@admin.register(AuthorCertification)
class AuthorCertificationAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "issuer", "issue_date", "created_at", "updated_at")
    search_fields = ("author__username", "author__email", "author__contact_no")
    ordering = ("-id",)
    list_per_page = 20
