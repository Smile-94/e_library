import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.book.models.category_model import Category
from apps.subscription.models.user_subscription_model import (
    UserSubscription,
    UserSubscriptionPaymentStatus,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class MySubscriptionHistoryView(LoginRequiredMixin, View):
    template_name = "home_user_subscription.html"
    model_class = UserSubscription

    def get(self, request):
        try:
            subscriptions = self.model_class.objects.filter(
                user=request.user, payment_status=UserSubscriptionPaymentStatus.PAID.value
            ).order_by("-id")
            context = {
                "title": "My Subscription History",
                "subscriptions": subscriptions,
                "show_hero_banner": False,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in My Subscription History View: {e}")
            messages.error(request, "Unable to load My Subscription History!")
            return HttpResponse(f"{e}")
            return HttpResponse(f"{e}")
