import logging

from django.contrib import messages

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin

# Django Response Class
from django.http import HttpResponse
from django.shortcuts import render

# Django View Classes
from django.views import View

from apps.account.models.user_model import User

from apps.book.models.book_model import Book
from apps.order.models.order_model import Order, OrderStatusChoices

# Custom Permission Class
from apps.common.permissions import StaffPassesTestMixin

logger = logging.getLogger(__name__)


class AdminDashboardView(LoginRequiredMixin, StaffPassesTestMixin, View):
    template_name = "dashboard.html"  # your template path
    user_model = User

    def get(self, request):
        try:
            total_customer = self.user_model.objects.filter(is_staff=False).count()
            total_staff = self.user_model.objects.filter(is_staff=True).count()
            total_author = self.user_model.objects.filter(is_author=True).count()
            total_books = Book.objects.all().count()
            recent_orders = Order.objects.filter(status=OrderStatusChoices.PENDING.value).order_by("-id")[:5]
            context = {
                "title": "Dashboard",
                "total_customer": total_customer,
                "total_staff": total_staff,
                "total_author": total_author,
                "total_books": total_books,
                "recent_orders": recent_orders,
            }

            return render(request, self.template_name, context)
            # return HttpResponse(f"Hello {context['name']}")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error orccured in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load dashboard!")
            return HttpResponse("Something went wrong!")
