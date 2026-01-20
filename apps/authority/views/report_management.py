from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from apps.order.models.order_model import Order
import logging
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_date, parse_time
from django.utils.timezone import make_aware, datetime as dt
from apps.subscription.models.user_subscription_model import UserSubscription

logger = logging.getLogger(__name__)


# <<------------------------------------>>> Daily Sales Report View <<------------------------------------>>
class DailySalesReportView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_daily_sales_report"
    template_name = "report/daily_sales_report.html"
    model_class = Order

    def get(self, request):
        try:
            # Get filter dates from GET params
            from_date = request.GET.get("from_date")
            to_date = request.GET.get("to_date")

            orders_qs = self.model_class.objects.all()

            if from_date:
                orders_qs = orders_qs.filter(created_at__date__gte=parse_date(from_date))
            if to_date:
                orders_qs = orders_qs.filter(created_at__date__lte=parse_date(to_date))

            # Aggregate daily totals
            report = (
                orders_qs.annotate(date=TruncDate("created_at"))
                .values("date")
                .annotate(
                    total_orders=Count("id"),
                    pending=Count("id", filter=Q(status="pending")),
                    pending_amount=Sum("net_amount", filter=Q(status="pending")),
                    confirmed=Count("id", filter=Q(status="confirmed")),
                    confirmed_amount=Sum("net_amount", filter=Q(status="confirmed")),
                    shipped=Count("id", filter=Q(status="shipped")),
                    shipped_amount=Sum("net_amount", filter=Q(status="shipped")),
                    delivered=Count("id", filter=Q(status="delivered")),
                    delivered_amount=Sum("net_amount", filter=Q(status="delivered")),
                    cancelled=Count("id", filter=Q(status="cancelled")),
                    cancelled_amount=Sum("net_amount", filter=Q(status="cancelled")),
                    total_amount=Sum("net_amount"),
                )
                .order_by("-date")
            )

            # Compute grand totals
            grand_total = {
                "total_orders": sum(row["total_orders"] for row in report),
                "pending": sum(row["pending"] for row in report),
                "pending_amount": sum(row["pending_amount"] or 0 for row in report),
                "confirmed": sum(row["confirmed"] for row in report),
                "confirmed_amount": sum(row["confirmed_amount"] or 0 for row in report),
                "shipped": sum(row["shipped"] for row in report),
                "shipped_amount": sum(row["shipped_amount"] or 0 for row in report),
                "delivered": sum(row["delivered"] for row in report),
                "delivered_amount": sum(row["delivered_amount"] or 0 for row in report),
                "cancelled": sum(row["cancelled"] for row in report),
                "cancelled_amount": sum(row["cancelled_amount"] or 0 for row in report),
                "total_amount": sum(row["total_amount"] or 0 for row in report),
            }

            context = {
                "title": "Daily Sales Report",
                "table_title": "Daily Sales Report",
                "report": report,
                "from_date": from_date,
                "to_date": to_date,
                "grand_total": grand_total,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR: Error in Daily Sales Report View: {e}")
            messages.error(request, "Unable to load Daily Sales Report!")
            return HttpResponse(f"{e}")


# <<------------------------------------>>> Invoice Sales Report View <<------------------------------------>>
class InvoiceSalesReportView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_invoice_sales_report"
    template_name = "report/invoice_sales_report.html"
    model_class = Order

    def get(self, request):
        try:
            date_str = request.GET.get("date")  # Specific date
            time_from_str = request.GET.get("time_from")  # Start time
            time_to_str = request.GET.get("time_to")  # End time

            orders_qs = self.model_class.objects.select_related("user")

            if date_str:
                date_obj = parse_date(date_str)

                if time_from_str:
                    time_from_obj = parse_time(time_from_str)
                else:
                    time_from_obj = dt.min.time()  # 00:00

                if time_to_str:
                    time_to_obj = parse_time(time_to_str)
                else:
                    time_to_obj = dt.max.time()  # 23:59:59

                # Make timezone-aware datetime objects
                start_datetime = make_aware(dt.combine(date_obj, time_from_obj))
                end_datetime = make_aware(dt.combine(date_obj, time_to_obj))

                orders_qs = orders_qs.filter(created_at__gte=start_datetime, created_at__lte=end_datetime)

            # Order by latest
            orders_qs = orders_qs.order_by("-created_at")

            # Compute grand totals
            grand_total_agg = orders_qs.aggregate(
                total_price=Sum("total_price"),
                total_discount=Sum("total_discount"),
                shipping_charge=Sum("shipping_charge"),
                net_amount=Sum("net_amount"),
            )

            grand_total = {
                "total_price": grand_total_agg["total_price"] or 0,
                "total_discount": grand_total_agg["total_discount"] or 0,
                "shipping_charge": grand_total_agg["shipping_charge"] or 0,
                "net_amount": grand_total_agg["net_amount"] or 0,
            }

            context = {
                "title": "Invoice-wise Sales Report",
                "table_title": "Invoice-wise Sales Report",
                "orders": orders_qs,
                "date": date_str,
                "time_from": time_from_str,
                "time_to": time_to_str,
                "grand_total": grand_total,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR: Error in Invoice Sales Report View: {e}")
            messages.error(request, "Unable to load Invoice-wise Sales Report!")
            return HttpResponse(f"{e}")


# <<------------------------------------>>> Daily Subscription Report View <<------------------------------------>>
class DailySubscriptionReportView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_subscription_report"
    template_name = "report/daily_subscription_report.html"
    model_class = UserSubscription

    def get(self, request):
        try:
            from_date = request.GET.get("from_date")
            to_date = request.GET.get("to_date")

            subscriptions_qs = self.model_class.objects.select_related("subscription").all()

            if from_date:
                subscriptions_qs = subscriptions_qs.filter(start_at__date__gte=from_date)
            if to_date:
                subscriptions_qs = subscriptions_qs.filter(start_at__date__lte=to_date)

            # Aggregate daily totals
            report = (
                subscriptions_qs.annotate(date=TruncDate("start_at"))
                .values("date")
                .annotate(
                    total_subscriptions=Count("id"),
                    active_count=Count("id", filter=Q(active_status="active")),
                    paid_count=Count("id", filter=Q(payment_status="paid")),
                    unpaid_count=Count("id", filter=Q(payment_status="unpaid")),
                    failed_count=Count("id", filter=Q(payment_status="failed")),
                    paid_amount=Sum(F("subscription__subscription_price"), filter=Q(payment_status="paid")),
                    unpaid_amount=Sum(F("subscription__subscription_price"), filter=Q(payment_status="unpaid")),
                    failed_amount=Sum(F("subscription__subscription_price"), filter=Q(payment_status="failed")),
                    total_amount=Sum(F("subscription__subscription_price")),
                )
                .order_by("-date")
            )

            # Compute grand totals
            grand_total = {
                "total_subscriptions": sum(row["total_subscriptions"] for row in report),
                "active_count": sum(row["active_count"] for row in report),
                "paid_count": sum(row["paid_count"] for row in report),
                "unpaid_count": sum(row["unpaid_count"] for row in report),
                "failed_count": sum(row["failed_count"] for row in report),
                "paid_amount": sum(row["paid_amount"] or 0 for row in report),
                "unpaid_amount": sum(row["unpaid_amount"] or 0 for row in report),
                "failed_amount": sum(row["failed_amount"] or 0 for row in report),
                "total_amount": sum(row["total_amount"] or 0 for row in report),
            }

            context = {
                "title": "Daily Subscription Report",
                "table_title": "Daily Subscription Report",
                "report": report,
                "from_date": from_date,
                "to_date": to_date,
                "grand_total": grand_total,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR: Daily Subscription Report: {e}")
            messages.error(request, "Unable to load Daily Subscription Report!")
            return HttpResponse(f"{e}")
