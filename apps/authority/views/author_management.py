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
from apps.author.models.author_model import AuthorWorkExperience

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
                user.save()
                messages.success(request, "Author created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Author",
                "form_title": "Create Author",
                "form": form,
            }
            messages.error(request, "Unable to create staff!")
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
