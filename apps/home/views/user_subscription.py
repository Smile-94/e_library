import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views import View

from apps.book.models.book_model import Book
from apps.book.models.category_model import Category
from apps.common.models import ActiveStatusChoices
from apps.subscription.models.subscription_model import SubscriptionReadLimitChoices
from apps.subscription.models.user_subscription_model import (
    UserSubscription,
    UserSubscriptionBooks,
    UserSubscriptionPaymentStatus,
)

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** My Subscription History View ***------------------------------------>>
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


# <<------------------------------------*** Add Book To My Subscription View ***------------------------------------>>
class AddBookToMySubscriptionView(LoginRequiredMixin, View):
    login_url = "account:login"  # your login URL name
    model_class = UserSubscription

    def handle_no_permission(self):
        # AJAX request → redirect explicitly
        return JsonResponse({"status": "unauthenticated", "redirect_url": reverse(self.login_url)}, status=401)

    def post(self, request):
        try:
            book_id = request.POST.get("book_id")
            book_instance = Book.objects.filter(id=book_id).first()
            current_time = now()

            user_subscription = (
                self.model_class.objects.select_related("subscription")
                .filter(
                    user=request.user,
                    active_status=ActiveStatusChoices.ACTIVE,
                    payment_status=UserSubscriptionPaymentStatus.PAID,
                    start_at__lte=current_time,
                    end_at__gte=current_time,
                )
                .first()
            )

            if not user_subscription:
                return JsonResponse({"status": "error", "message": "No active subscription found"}, status=400)

            subscription = user_subscription.subscription

            if subscription.book_read_limit == SubscriptionReadLimitChoices.LIMITED:
                if user_subscription.read_count >= subscription.max_book_read_limit:
                    return JsonResponse({"status": "error", "message": "Book read limit exceeded"}, status=400)

            if book_instance and not book_instance.digital_file:
                return JsonResponse({"status": "error", "message": "Book does not have digital file"}, status=400)

            if UserSubscriptionBooks.objects.filter(user_subscription=user_subscription, book_id=book_id).exists():
                return JsonResponse({"status": "error", "message": "Book already added"}, status=400)

            with transaction.atomic():
                UserSubscriptionBooks.objects.create(
                    user_subscription=user_subscription,
                    book_id=book_id,
                )
                user_subscription.read_count += 1
                user_subscription.save(update_fields=["read_count"])

            return JsonResponse({"status": "success", "message": "Book added to My Books"})

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in AddBookToMySubscriptionView: {e}")
            return JsonResponse({"status": "error", "message": "Something went wrong"}, status=500)


# <<------------------------------------*** My Subscription Book List View ***------------------------------------>>
class MySubscriptionBookListView(LoginRequiredMixin, View):
    login_url = "account:login"  # your login URL name
    model_class = UserSubscription
    template_name = "my_subscription_book.html"

    def get(self, request):
        try:
            user_subscription = self.model_class.objects.filter(user=request.user).order_by("-id").first()

            if not user_subscription:
                messages.error(request, "You don't have any subscriptions!")
                return redirect("home:index")

            my_books = UserSubscriptionBooks.objects.filter(user_subscription=user_subscription).order_by("-id")

            context = {
                "title": "My Subscription Book List",
                "user_subscription": user_subscription,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
                "show_hero_banner": False,
                "books": my_books,
                "latest_books": Book.objects.all().order_by("-id"),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in MySubscriptionBookListView: {e}")
            messages.error(request, "Unable to load My Subscription Book List!")
            return HttpResponse(f"{e}")
