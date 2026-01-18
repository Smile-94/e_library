import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from apps.order.models.discount_model import PromotionalDiscount
from apps.order.filters.discount_filter import PromotionalDiscountSearchFilter
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)


# <<------------------------------------*** Promotional Discount List View ***------------------------------------>>
class PromotionalDiscountListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_promotional_discount"
    template_name = "discount/discount_list.html"
    model_class = PromotionalDiscount
    filter_class = PromotionalDiscountSearchFilter

    def get(self, request):
        try:
            discounts = (
                self.model_class.objects.select_related()
                .prefetch_related("discount_category", "discount_book")
                .order_by("-priority", "-id")
            )

            context = {
                "title": "Promotional Discount List",
                "table_title": "Promotional Discount List",
                "discounts": self.filter_class(request.GET, queryset=discounts),
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount List View: {e}")
            messages.error(request, "Unable to load Promotional Discount list!")
            return HttpResponse(f"{e}")
