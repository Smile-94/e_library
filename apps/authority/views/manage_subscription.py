import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin
from apps.subscription.filters.subscription_filter import (
    SubscriptionSearchFilter,
    UserSubscriptionSearchFilter,
)
from apps.subscription.forms.subscription_form import (
    SubscriptionForm,
    UserSubscriptionForm,
)
from apps.subscription.models.subscription_model import Subscription
from apps.subscription.models.user_subscription_model import UserSubscription

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** Manage Subscription Create View ***------------------------------------>>
class SubscriptionCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_subscription"
    template_name = "subscription_create.html"
    model_class = Subscription
    form_class = SubscriptionForm
    success_url = reverse_lazy("authority:subscription_list")

    def get(self, request):
        try:
            context = {
                "title": "Create Subscription",
                "form_title": "Create Subscription",
                "form": self.form_class(),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Create GET View: {e}")
            messages.error(request, "Unable to load Manage Subscription details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                subscription = form.save()
                subscription.created_by = request.user
                subscription.save()
                messages.success(request, "Subscription created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Subscription",
                "form_title": "Create Subscription",
                "form": form,
            }
            messages.error(request, "Unable to create Subscription!")
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Create POST View: {e}")
            messages.error(request, "Unable to create Subscription!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Manage Subscription Edit View ***------------------------------------>>
class SubscriptionEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_subscription"
    template_name = "edit_subscription.html"
    model_class = Subscription
    form_class = SubscriptionForm

    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = self.model_class.objects.filter(pk=pk).first()

            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("authority:manage_subscription_list")

            context = {
                "title": "Edit Subscription",
                "form_title": "Edit Subscription",
                "form": self.form_class(instance=subscription),
                "subscription_obj": subscription,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Edit GET View: {e}")
            messages.error(request, "Unable to load Manage Subscription details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            subscription = self.model_class.objects.filter(pk=pk).first()

            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("authority:subscription_list")

            form = self.form_class(request.POST, request.FILES, instance=subscription)

            if not form.is_valid():
                context = {
                    "title": "Edit Subscription",
                    "form_title": "Edit Subscription",
                    "form": form,
                    "subscription_obj": subscription,
                }
                messages.error(request, "Unable to update Subscription!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Subscription updated successfully!")
            return redirect("authority:subscription_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Edit POST View: {e}")
            messages.error(request, "Unable to update Subscription!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Manage Subscription List View ***------------------------------------>>
class SubscriptionListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_subscription"
    template_name = "subscription_list.html"
    model_class = Subscription
    filter_class = SubscriptionSearchFilter

    def get(self, request):
        try:
            subscriptions = self.model_class.objects.all().order_by("id")

            context = {
                "title": "Subscription List",
                "table_title": "Subscription List",
                "data_list": self.filter_class(request.GET, queryset=subscriptions),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription List View: {e}")
            messages.error(request, "Unable to load Subscription list!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Manage Subscription Detail View ***------------------------------------>>
class SubscriptionDetailView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_subscription"
    model_class = Subscription
    template_name = "subscription_detail.html"

    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = self.model_class.objects.filter(pk=pk).first()
            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("authority:manage_subscription_list")

            context = {
                "title": "Subscription Details",
                "subscription_obj": subscription,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Detail View: {e}")
            messages.error(request, "Unable to load Subscription details!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Manage Subscription Soft Delete View ***------------------------------------>>
class SubscriptionSoftDeleteView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_delete_subscription"
    model_class = Subscription
    template_name = "subscription_delete.html"

    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = self.model_class.objects.filter(pk=pk).first()
            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("authority:manage_subscription_list")

            context = {
                "title": "Delete Subscription",
                "form_title": "Delete Subscription",
                "object": subscription,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Soft Delete View: {e}")
            messages.error(request, "Unable to load Subscription details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk, *args, **kwargs):
        try:
            subscription = self.model_class.objects.filter(pk=pk).first()
            if not subscription:
                messages.error(request, "Subscription not found!")
                return redirect("authority:manage_subscription_list")

            subscription.is_deleted = True
            subscription.save()

            messages.success(request, "Subscription deleted successfully!")
            return redirect("authority:manage_subscription_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Soft Delete View: {e}")
            messages.error(request, "Unable to delete Subscription!")
            return HttpResponse(f"{e}")


# <<------------------------------------***User Subscription List View***------------------------------------>>
class UserSubscriptionListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_user_subscription"
    template_name = "user_subscription_list.html"
    model_class = UserSubscription
    filter_class = UserSubscriptionSearchFilter

    def get(self, request):
        try:
            user_subscriptions = self.model_class.objects.all().order_by("-id")
            context = {
                "title": "User Subscription List",
                "table_title": "User Subscription List",
                "data_list": self.filter_class(request.GET, queryset=user_subscriptions),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription List View: {e}")
            messages.error(request, "Unable to load Subscription list!")
            return HttpResponse(f"{e}")


# <<------------------------------------***User Subscription Edit View***------------------------------------>>
class UserSubscriptionEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_user_subscription"
    template_name = "user_subscription_edit.html"
    model_class = UserSubscription
    form_class = UserSubscriptionForm

    def get(self, request, pk, *args, **kwargs):
        try:
            user_subscription = self.model_class.objects.filter(pk=pk).first()
            if not user_subscription:
                messages.error(request, "User Subscription not found!")
                return redirect("authority:user_subscription_list")

            context = {
                "title": "Edit User Subscription",
                "form_title": "Edit User Subscription",
                "form": self.form_class(instance=user_subscription),
                "user_subscription_obj": user_subscription,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Edit View: {e}")
            messages.error(request, "Unable to load Manage Subscription details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            user_subscription = self.model_class.objects.filter(pk=pk).first()

            if not user_subscription:
                messages.error(request, "User Subscription not found!")
                return redirect("authority:user_subscription_list")

            form = self.form_class(request.POST, request.FILES, instance=user_subscription)

            if not form.is_valid():
                context = {
                    "title": "Edit User Subscription",
                    "form_title": "Edit User Subscription",
                    "form": form,
                    "user_subscription_obj": user_subscription,
                }
                print(form.errors)
                messages.error(request, "Unable to update User Subscription!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "User Subscription updated successfully!")
            return redirect("authority:user_subscription_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Manage Subscription Edit View: {e}")
            messages.error(request, "Unable to update User Subscription!")
            return HttpResponse(f"{e}")
