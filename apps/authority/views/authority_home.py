import logging

from django.contrib import messages

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin

# Django Response Class
from django.http import HttpResponse
from django.shortcuts import render

# Django View Classes
from django.views import View

# Custom Permission Class
from apps.common.permissions import StaffPassesTestMixin

logger = logging.getLogger(__name__)


class AdminDashboardView(LoginRequiredMixin, StaffPassesTestMixin, View):
    template_name = "dashboard.html"  # your template path

    def get(self, request):
        try:
            context = {
                "title": "Dashboard",
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error orccured in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load dashboard!")
            return HttpResponse("Something went wrong!")
