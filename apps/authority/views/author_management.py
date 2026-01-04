import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.account.forms.user_forms import UserForm
from apps.author.forms.education_forms import AuthorEducationForm
from apps.author.forms.exprience_forms import AuthorWorkExperienceForm
from apps.author.function.unique_username import unique_hex_username
from apps.author.models.author_model import AuthorEducation, AuthorWorkExperience

# Import Filters
from apps.authority.filters.user_filter import UserSearchFilter
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)
User = get_user_model()


# * <<------------------------------------*** Author Create User View ***------------------------------------>>
class AuthorCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_author"
    template_name = "author_create.html"
    model_class = User
    form_class = UserForm
    success_url = reverse_lazy("authority:author_list")

    def get(self, request):
        try:
            context = {
                "title": "Create Author",
                "form_title": "Create Author",
                "user_form": self.form_class(),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Create GET View: {e}")
            messages.error(request, "Unable to load staff details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                user.is_author = True
                if not form.cleaned_data.get("username"):
                    user.username = unique_hex_username()
                user.save()
                messages.success(request, "Author created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Author",
                "form_title": "Create Author",
                "user_form": self.form_class(),
            }
            messages.error(request, "Unable to create Author!")
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Create POST View: {e}")
            messages.error(request, "Unable to create staff!")
            return HttpResponse(f"{e}")


# * <<------------------------------------*** Author User Edit View ***------------------------------------>>
class AuthorEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_author"
    template_name = "author_edit.html"
    model_class = User
    form_class = UserForm

    def get(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk, is_author=True).first()

            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Edit Author",
                "form_title": "Edit Author",
                "user_form": self.form_class(instance=user),
                "user_obj": user,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Edit GET View: {e}")
            messages.error(request, "Unable to edit Author!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            user = self.model_class.objects.filter(pk=pk, is_author=True).first()
            form = UserForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, "Author updated successfully!")
                return redirect("authority:author_list")

            context = {
                "title": "Edit Author",
                "form_title": "Edit Author",
                "user_form": self.form_class(instance=user),
                "user_obj": user,
            }
            messages.error(request, "Unable to update staff!")
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Edit GET View: {e}")
            messages.error(request, "Unable to update Author!")
            return HttpResponse(f"{e}")


# * <<------------------------------------*** Author List User View ***------------------------------------>>
class AuthorListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_author"
    template_name = "author_list.html"
    model_class = User
    filter_class = UserSearchFilter

    def get(self, request):
        try:
            users = self.model_class.objects.filter(is_deleted=False, is_author=True).order_by("id")

            context = {
                "title": "Author List",
                "table_title": "Author List",
                "users": self.filter_class(request.GET, queryset=users),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author List View: {e}")
            messages.error(request, "Unable to load Author list!")
            return HttpResponse(f"{e}")


# * << ------------------------------------*** Author User Detail View ***------------------------------------ >>
class AuthorDetailView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_author"
    model_class = User
    template_name = "author_detail.html"

    def get(self, request, pk):
        try:
            # Fetch the staff user or 404 if not found or soft-deleted
            user_obj = (
                self.model_class.objects.filter(pk=pk, is_author=True)
                .prefetch_related(
                    Prefetch(
                        "author_work_experiences",
                        queryset=AuthorWorkExperience.objects.all().order_by("id"),
                        to_attr="experiences",
                    ),
                    Prefetch(
                        "author_educations",
                        queryset=AuthorEducation.objects.all().order_by("id"),
                        to_attr="educations",
                    ),
                )
                .first()
            )
            if not user_obj:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Author Details",
                "user_obj": user_obj,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in author Detail View: {e}")
            messages.error(request, "Unable to load author details!")
            return redirect("authority:author_list")


# * << ------------------------------------*** Author User Soft Delete View ***------------------------------------ >>
class AuthorSoftDeleteView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_delete_author"
    model_class = User
    template_name = "author_delete.html"

    def get(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk, is_author=True).first()
            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Delete Author",
                "form_title": "Delete Author",
                "object": user,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in author Delete GET View: {e}")
            messages.error(request, "Unable to load author details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk, is_staff=True).first()
            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            user.is_deleted = True
            user.save()

            messages.success(request, "Author deleted successfully!")
            return redirect("authority:author_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in author Soft Delete View: {e}")
            messages.error(request, "Unable to delete author!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Author Work Experience Create View ***------------------------------------>>
class AuthorWorkExperienceCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_author_experience"
    template_name = "author_experience_create.html"
    model_class = User
    form_class = AuthorWorkExperienceForm

    def get(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk, is_author=True).first()
            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Add Author Work Experience",
                "form_title": "Add Author Work Experience",
                "form": self.form_class(),
                "user_obj": user,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Work Experience Create GET View: {e}")
            messages.error(request, "Unable to load Author Work Experience details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk).first()

            form = self.form_class(request.POST)
            if form.is_valid():
                author_work_experience = form.save(commit=False)
                author_work_experience.author = user
                author_work_experience.save()

                messages.success(request, "Author Work Experience created successfully!")
                return redirect("authority:author_detail", pk=user.pk)

            messages.error(request, "Unable to create Author Work Experience!")
            return render(
                request,
                self.template_name,
                {
                    "title": "Add Author Work Experience",
                    "form_title": "Add Author Work Experience",
                    "form": form,
                    "user_obj": user,
                },
            )

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Work Experience Create POST View: {e}")
            messages.error(request, "Unable to create Author Work Experience!")
            return HttpResponse(str(e))


# <<------------------------------------*** Author Work Experience Edit View ***------------------------------------>>
class AuthorWorkExperienceEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_author_experience"
    template_name = "edit_author_experience.html"
    model_class = AuthorWorkExperience
    form_class = AuthorWorkExperienceForm

    def get(self, request, pk, *args, **kwargs):
        try:
            work_experience = self.model_class.objects.filter(pk=pk).first()
            if not work_experience:
                messages.error(request, "Author Work Experience not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Edit Author Work Experience",
                "form_title": "Edit Author Work Experience",
                "form": self.form_class(instance=work_experience),
                "user_obj": work_experience.author,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Work Experience Edit GET View: {e}")
            messages.error(request, "Unable to load Author Work Experience details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            work_experience = self.model_class.objects.filter(pk=pk).first()
            if not work_experience:
                messages.error(request, "Author Work Experience not found!")
                return redirect("authority:author_list")

            form = self.form_class(request.POST, request.FILES, instance=work_experience)

            if not form.is_valid():
                context = {
                    "title": "Create Author Work Experience",
                    "form_title": "Create Author Work Experience",
                    "user_form": self.form_class(instance=work_experience),
                    "user_obj": work_experience.author,
                }
                messages.error(request, "Unable to update Author Work Experience!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Author Work Experience updated successfully!")
            return redirect("authority:author_detail", pk=work_experience.author.pk)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Work Experience Edit POST View: {e}")
            messages.error(request, "Unable to update Author Work Experience!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Author Education Create View ***------------------------------------>>
class AuthorEducationCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_author_education"
    template_name = "author_education_create.html"
    model_class = User
    form_class = AuthorEducationForm

    def get(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk).first()

            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            context = {
                "title": "Add Author Education",
                "form_title": "Add Author Education",
                "form": self.form_class(),
                "user_obj": user,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Education Create GET View: {e}")
            messages.error(request, "Unable to load Author Education details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk).first()

            if not user:
                messages.error(request, "Author not found!")
                return redirect("authority:author_list")

            form = self.form_class(request.POST)
            if form.is_valid():
                author_education = form.save(commit=False)
                author_education.author = user
                author_education.save()

                messages.success(request, "Author Education created successfully!")
                return redirect("authority:author_detail", pk=user.pk)

            messages.error(request, "Unable to create Author Education!")
            return render(
                request,
                self.template_name,
                {
                    "title": "Add Author Education",
                    "form_title": "Add Author Education",
                    "form": form,
                    "user_obj": user,
                },
            )

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Education Create POST View: {e}")
            messages.error(request, "Unable to create Author Education!")
            return HttpResponse(str(e))


# <<------------------------------------*** Author Education Edit View ***------------------------------------>>
class AuthorEducationEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_author_education"
    template_name = "edit_author_education.html"
    model_class = AuthorEducation
    form_class = AuthorEducationForm

    def get(self, request, pk, *args, **kwargs):
        try:
            education = self.model_class.objects.filter(pk=pk).first()

            if not education:
                messages.error(request, "Author Education not found!")
                return redirect("authority:author_detail", pk=pk)

            context = {
                "title": "Edit Author Education",
                "form_title": "Edit Author Education",
                "form": self.form_class(instance=education),
                "user_obj": education.author,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Education Edit GET View: {e}")
            messages.error(request, "Unable to load Author Education details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            education = self.model_class.objects.filter(pk=pk).first()

            if not education:
                messages.error(request, "Author Education not found!")
                return redirect("authority:author_detail", pk=pk)

            form = self.form_class(request.POST, request.FILES, instance=education)

            if not form.is_valid():
                context = {
                    "title": "Edit Author Education",
                    "form_title": "Edit Author Education",
                    "form": form,
                    "user_obj": education.author,
                }
                messages.error(request, "Unable to update Author Education!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Author Education updated successfully!")
            return redirect("authority:author_detail", pk=education.author.pk)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Author Education Edit POST View: {e}")
            messages.error(request, "Unable to update Author Education!")
            return HttpResponse(str(e))
