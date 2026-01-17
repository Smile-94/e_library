import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.order.models.order_model import Order

logger = logging.getLogger(__name__)


# <<------------------------------------*** My Orders View ***------------------------------------>>
class MyOrdersView(LoginRequiredMixin, View):
    login_url = "account:login"
    template_name = "my_order_history.html"

    def get(self, request):
        try:
            orders = Order.objects.filter(user=request.user).order_by("-created_at")
            context = {
                "title": "My Orders",
                "orders": orders,
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in My Orders View: {e}")
            messages.error(request, "Unable to load My Orders!")
            return redirect("home:home")


# <<------------------------------------*** Order Detail View ***------------------------------------>>
class OrderDetailView(LoginRequiredMixin, View):
    login_url = "account:login"
    template_name = "my_order_details.html"

    def get(self, request, pk):
        try:
            order = Order.objects.filter(pk=pk).first()
            if not order:
                messages.error(request, "Order not found!")
                return redirect("home:home")

            order_products = order.order_placed_products.all()
            context = {
                "title": f"Order #{order.invoice_id}",
                "order": order,
                "order_products": order_products,
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Order Detail View: {e}")
            messages.error(request, "Unable to load Order Detail!")
            return redirect("home:home")
