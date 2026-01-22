import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.order.filters.order_filter import OrderSearchFilter
from apps.order.models.order_model import Order
from django.db.models import Case, When, Value, IntegerField
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin
from django.shortcuts import redirect
from django.template.loader import get_template
from weasyprint import HTML
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# <<------------------------------------>>> Order List View <<------------------------------------>>
class OrderListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_order"
    template_name = "order/order_list.html"
    model_class = Order
    filter_class = OrderSearchFilter

    def get(self, request):
        try:
            orders = (
                self.model_class.objects.select_related("user")
                .annotate(
                    pending_order=Case(
                        When(status="pending", then=Value(0)),  # pending first
                        default=Value(1),  # others later
                        output_field=IntegerField(),
                    )
                )
                .order_by("pending_order", "-id")
            )

            filterset = self.filter_class(request.GET, queryset=orders)

            context = {
                "title": "Order List",
                "table_title": "Order List",
                "orders": filterset,  # filtered queryset
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR: Error in Order List View: {e}")
            messages.error(request, "Unable to load Order list!")
            return HttpResponse(f"{e}")


# <<------------------------------------>>> Order Detail View <<------------------------------------>>
class OrderDetailView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_order"
    template_name = "order/order_details.html"
    model_class = Order

    def get(self, request, pk):
        """
        Display details of a single order
        """
        try:
            order = (
                self.model_class.objects.filter(pk=pk)
                .select_related("user", "order_shipping_address", "payment_info")
                .prefetch_related("order_placed_products__product")
                .first()
            )
            if not order:
                messages.error(request, "Order not found!")
                return redirect("authority:order_list")

            context = {
                "title": f"Order #{order.invoice_id} Details",
                "order": order,
                "statuses": Order._meta.get_field("status").choices,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR: Failed to load Order Detail view: {e}")
            messages.error(request, "Unable to load order details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        order = self.model_class.objects.filter(pk=pk).first()
        if not order:
            messages.error(request, "Order not found!")
            return redirect("authority:order_list")

        new_status = request.POST.get("status")

        if new_status not in dict(Order._meta.get_field("status").choices):
            messages.error(request, "Invalid order status selected.")
            return redirect("authority:order_detail", pk=pk)

        order.status = new_status
        order.save(update_fields=["status"])
        messages.success(request, f"Order status updated to {order.get_status_display()}.")
        return redirect("authority:order_list")  # Redirect to Order List after update


# <<------------------------------------*** Order PDF View ***------------------------------------>>
class OrderPDFView(View):
    """
    Generate PDF for a given Order using WeasyPrint.
    """

    template_name = "order/order_detail_pdf.html"
    model_class = Order  # Model class to fetch the order from

    def get(self, request, order_id, *args, **kwargs):
        try:
            # Fetch the order object
            order = self.model_class.objects.filter(pk=order_id).prefetch_related("order_placed_products__product").first()

            # Render template to HTML string
            html_string = render_to_string(self.template_name, {"order": order}, request=request)

            # Convert HTML to PDF
            pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

            # Return PDF in HTTP response
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="order_{order.invoice_id}.pdf"'
            return response

        except Exception as e:
            logger.exception(f"Failed to generate PDF for Order ID {order_id}: {e}")
            return HttpResponse("An error occurred while generating PDF. Please try again later.")


# <<------------------------------------*** Order Packing Slip View ***------------------------------------>>
class OrderPackingSlipView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_order"
    template_name = "order/order_packing_pdf.html"
    model_class = Order

    def get(self, request, order_id, *args, **kwargs):
        try:
            # Fetch the order object
            order = self.model_class.objects.filter(pk=order_id).prefetch_related("order_placed_products__product").first()

            # Render template to HTML string
            html_string = render_to_string(self.template_name, {"order": order}, request=request)

            # Convert HTML to PDF
            pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

            # Return PDF in HTTP response
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="order_{order.invoice_id}.pdf"'
            return response

        except Exception as e:
            logger.exception(f"Failed to generate PDF for Order ID {order_id}: {e}")
            return HttpResponse("An error occurred while generating PDF. Please try again later.")
