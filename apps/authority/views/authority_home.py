import logging

from django.contrib import messages

# Permission and Authentication
from django.contrib.auth.mixins import LoginRequiredMixin

# Django Response Class
from django.http import HttpResponse
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from datetime import timedelta
from apps.book.models.category_model import Category

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

            today = now().date()
            last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

            orders_qs = (
                Order.objects.filter(
                    created_at__date__gte=last_7_days[0],
                    status__in=[
                        OrderStatusChoices.PENDING,
                        OrderStatusChoices.CONFIRMED,
                        OrderStatusChoices.DELIVERED,
                    ],
                )
                .annotate(day=TruncDate("created_at"))
                .values("day", "status")
                .annotate(count=Count("id"))
            )

            # Prepare default structure
            weekly_data = {
                "labels": [day.strftime("%d %b") for day in last_7_days],
                "pending": [0] * 7,
                "confirmed": [0] * 7,
                "delivered": [0] * 7,
            }

            day_index_map = {day: idx for idx, day in enumerate(last_7_days)}

            for item in orders_qs:
                idx = day_index_map[item["day"]]
                if item["status"] == OrderStatusChoices.PENDING:
                    weekly_data["pending"][idx] = item["count"]
                elif item["status"] == OrderStatusChoices.CONFIRMED:
                    weekly_data["confirmed"][idx] = item["count"]
                elif item["status"] == OrderStatusChoices.DELIVERED:
                    weekly_data["delivered"][idx] = item["count"]

            # Get categories with at least 1 book
            category_data = (
                Category.objects.filter(active_status="active")
                .annotate(total_books=Count("books_category", filter=Q(books_category__isnull=False)))
                .filter(total_books__gt=0)  # Keep only categories with at least 1 book
                .values("category_name", "total_books")
            )

            pie_data = {
                "labels": [c["category_name"] for c in category_data],
                "data": [c["total_books"] for c in category_data],
            }

            context = {
                "title": "Dashboard",
                "total_customer": total_customer,
                "total_staff": total_staff,
                "total_author": total_author,
                "total_books": total_books,
                "recent_orders": recent_orders,
                "weekly_sales": weekly_data,
                "category_pie_data": pie_data,
            }

            return render(request, self.template_name, context)
            # return HttpResponse(f"Hello {context['name']}")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error orccured in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load dashboard!")
            return HttpResponse("Something went wrong!")
