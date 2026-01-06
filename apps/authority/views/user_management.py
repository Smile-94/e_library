import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Import Filters
from apps.authority.filters.user_filter import UserSearchFilter
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)
User = get_user_model()


class UserListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    template_name = "user_list.html"
    model_class = User
    filter_class = UserSearchFilter
    required_permission = "can_view_user"

    def get(self, request):
        try:
            users = self.model_class.objects.filter(is_staff=False, is_superuser=False, is_author=False, is_active=True).order_by("id")

            context = {
                "title": "User List",
                "table_title": "User List",
                "users": self.filter_class(request.GET, queryset=users),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in User List View: {e}")
            messages.error(request, "Unable to load user list!")
            return HttpResponse(f"{e}")
