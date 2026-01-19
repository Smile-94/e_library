import logging
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from apps.order.models.discount_model import PromotionalDiscount
from apps.order.filters.discount_filter import PromotionalDiscountSearchFilter
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin
from apps.order.form.discount_form import PromotionalDiscountForm
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


# <<------------------------------------*** Promotional Discount Create View ***------------------------------------>>
class PromotionalDiscountCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_promotional_discount"
    template_name = "discount/discount_create.html"
    form_class = PromotionalDiscountForm

    def get(self, request):
        try:
            context = {
                "title": "Create Promotional Discount",
                "form_title": "Create Promotional Discount",
                "form": self.form_class(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Create View: {e}")
            messages.error(request, "Unable to load Promotional Discount details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST)
            if not form.is_valid():
                context = {
                    "title": "Create Promotional Discount",
                    "form_title": "Create Promotional Discount",
                    "form": form,
                }
                messages.error(request, "Unable to create Promotional Discount!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Promotional Discount created successfully!")
            return redirect("authority:discount_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Create View: {e}")
            messages.error(request, "Unable to create Promotional Discount!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Promotional Discount Edit View ***------------------------------------>>
class PromotionalDiscountEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_promotional_discount"
    template_name = "discount/discount_edit.html"
    model_class = PromotionalDiscount
    form_class = PromotionalDiscountForm

    def get(self, request, pk, *args, **kwargs):
        try:
            discount = self.model_class.objects.filter(pk=pk).first()

            if not discount:
                messages.error(request, "Promotional Discount not found!")
                return redirect("authority:discount_list")

            context = {
                "title": "Edit Promotional Discount",
                "form_title": "Edit Promotional Discount",
                "form": self.form_class(instance=discount),
                "discount_obj": discount,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Edit GET View: {e}")
            messages.error(request, "Unable to load Promotional Discount details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            discount = self.model_class.objects.filter(pk=pk).first()

            if not discount:
                messages.error(request, "Promotional Discount not found!")
                return redirect("authority:discount_list")

            form = self.form_class(request.POST, request.FILES, instance=discount)

            if not form.is_valid():
                context = {
                    "title": "Edit Promotional Discount",
                    "form_title": "Edit Promotional Discount",
                    "form": form,
                    "discount_obj": discount,
                }
                messages.error(request, "Unable to update Promotional Discount!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Promotional Discount updated successfully!")
            return redirect("authority:discount_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Edit POST View: {e}")
            messages.error(request, "Unable to update Promotional Discount!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Promotional Discount List View ***------------------------------------>>
class PromotionalDiscountListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_promotional_discount"
    template_name = "discount/discount_list.html"
    model_class = PromotionalDiscount
    filter_class = PromotionalDiscountSearchFilter

    def get(self, request):
        try:
            discounts = (
                self.model_class.objects.select_related().prefetch_related("discount_category", "discount_book").order_by("-id")
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


# <<------------------------------------*** Promotional Discount Delete View ***------------------------------------>>
class PromotionalDiscountDeleteView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_delete_promotional_discount"
    model_class = PromotionalDiscount
    template_name = "discount/discount_delete.html"

    def get(self, request, pk, *args, **kwargs):
        try:
            discount = self.model_class.objects.filter(pk=pk).first()

            if not discount:
                messages.error(request, "Promotional Discount not found!")
                return redirect("authority:discount_list")

            context = {
                "title": "Delete Promotional Discount",
                "form_title": "Delete Promotional Discount",
                "object": discount,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Delete GET View: {e}")
            messages.error(request, "Unable to load Promotional Discount details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            discount = self.model_class.objects.filter(pk=pk).first()

            if not discount:
                messages.error(request, "Promotional Discount not found!")
                return redirect("authority:discount_list")

            discount.delete()

            messages.success(request, "Promotional Discount deleted successfully!")
            return redirect("authority:discount_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Promotional Discount Delete POST View: {e}")
            messages.error(request, "Unable to delete Promotional Discount!")
            return HttpResponse(f"{e}")
