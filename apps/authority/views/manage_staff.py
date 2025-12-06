import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.account.forms.user_forms import UserForm

# Import Filters
from apps.authority.filters.user_filter import UserSearchFilter
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)
User = get_user_model()


# * <<------------------------------------*** Staff Create User View ***------------------------------------>>
class StaffUserCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_staff"
    template_name = "staff_create.html"
    model_class = User
    form_class = UserForm
    success_url = reverse_lazy("authority:staff_list")

    def get(self, request):
        try:
            context = {
                "title": "Create Staff",
                "form_title": "Create Staff",
                "user_form": self.form_class(),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Create GET View: {e}")
            messages.error(request, "Unable to load staff details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                user.is_staff = True
                user.save()
                messages.success(request, "Staff created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Staff",
                "form_title": "Create Staff",
                "form": form,
            }
            messages.error(request, "Unable to create staff!")
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Create POST View: {e}")
            messages.error(request, "Unable to create staff!")
            return HttpResponse(f"{e}")


# * <<------------------------------------*** Staff User Edit View ***------------------------------------>>
class StaffUserEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_staff"
    template_name = "staff_edit.html"
    model_class = User
    form_class = UserForm

    def get(self, request, pk, *args, **kwargs):
        try:
            user = self.model_class.objects.filter(pk=pk, is_staff=True).first()

            if not user:
                messages.error(request, "Staff not found!")
                return redirect("authority:staff_list")

            context = {
                "title": "Edit Staff",
                "form_title": "Edit Staff",
                "user_form": self.form_class(instance=user),
                "user_obj": user,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Edit GET View: {e}")
            messages.error(request, "Unable to load staff details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            user = self.model_class.objects.filter(pk=pk, is_staff=True).first()
            form = UserForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, "Staff updated successfully!")
                return redirect("authority:staff_list")

            context = {
                "title": "Edit Staff",
                "form_title": "Edit Staff",
                "user_form": self.form_class(instance=user),
                "user_obj": user,
            }
            messages.error(request, "Unable to update staff!")
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Edit GET View: {e}")
            messages.error(request, "Unable to update staff!")
            return HttpResponse(f"{e}")


# * << ------------------------------------*** Staff User List View ***------------------------------------ >>
class StaffUserListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    template_name = "staff_list.html"
    model_class = User
    filter_class = UserSearchFilter
    required_permission = "can_view_staff"

    def get(self, request):
        try:
            users = self.model_class.objects.filter(is_staff=True, is_deleted=False).order_by("id")

            context = {
                "title": "Staff List",
                "table_title": "Staff List",
                "users": self.filter_class(request.GET, queryset=users),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in staff List View: {e}")
            messages.error(request, "Unable to load staff list!")
            return HttpResponse(f"{e}")


# * << ------------------------------------*** Staff User Detail View ***------------------------------------ >>
class StaffUserDetailView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_staff"
    model_class = User
    template_name = "staff_detail.html"

    def get(self, request, pk):
        try:
            # Fetch the staff user or 404 if not found or soft-deleted
            user_obj = self.model_class.objects.filter(pk=pk, is_staff=True).first()
            if not user_obj:
                messages.error(request, "Staff not found!")
                return redirect("authority:staff_list")

            context = {
                "title": "Staff Details",
                "user_obj": user_obj,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Detail View: {e}")
            messages.error(request, "Unable to load staff details!")
            return redirect("authority:staff_list")


# * << ------------------------------------*** Staff User Soft Delete View ***------------------------------------ >>
class StaffUserSoftDeleteView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_delete_staff"
    model_class = User
    template_name = "staff_delete.html"

    def get(self, request, pk):
        try:
            user = self.model_class.objects.filter(pk=pk, is_staff=True).first()
            if not user:
                messages.error(request, "Staff not found!")
                return redirect("authority:staff_list")

            context = {
                "title": "Delete Staff",
                "form_title": "Delete Staff",
                "object": user,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Staff Delete GET View: {e}")
            messages.error(request, "Unable to load staff details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            user = self.model_class.objects.filter(pk=pk, is_staff=True).first()
            if not user:
                messages.error(request, "Staff not found!")
                return redirect("authority:staff_list")

            user.is_deleted = True
            user.save()

            messages.success(request, "Staff deleted successfully!")
            return redirect("authority:staff_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in staff Soft Delete View: {e}")
            messages.error(request, "Unable to delete staff!")
            return HttpResponse(f"{e}")
