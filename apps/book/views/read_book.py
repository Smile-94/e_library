import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.book.models import Book
from apps.subscription.models import UserSubscriptionBooks
from apps.subscription.models.user_subscription_model import UserSubscriptionBooks
from apps.subscription.utils import get_active_subscription

logger = logging.getLogger(__name__)


# <<------------------------------------*** Read Book View ***------------------------------------>>
class SubscriptionBookReadView(LoginRequiredMixin, View):
    template_name = "read_book.html"
    model_class = Book
    user_subscription_book = UserSubscriptionBooks

    def get(self, request, book_id):
        try:
            book = self.model_class.objects.filter(id=book_id).first()

            if not book.digital_file:
                messages.error(request, "Book does not have digital file")
                return redirect("home:my_subscription_book_list")

            subscription = get_active_subscription(request.user)
            if not subscription:
                messages.error(request, "No active subscription found")
                return redirect("home:home_subscription")

            # Check or create subscription-book record
            sub_book, created = UserSubscriptionBooks.objects.get_or_create(
                user_subscription=subscription,
                book=book,
            )

            sub_book = self.user_subscription_book.objects.filter(user_subscription=subscription, book=book).first()
            if not sub_book:
                messages.error(request, "Book not added to subscription")
                return redirect("home:my_subscription_book_list")

            # Optional: enforce read limit
            MAX_READ = subscription.subscription.max_book_read_limit
            if MAX_READ and sub_book.read_count >= MAX_READ:
                messages.error(request, "Book read limit exceeded")
                return redirect("home:my_subscription_book_list")

            context = {
                "book": book,
                "title": f"Read: {book.title}",
                "hero_normal": "hero-normal",
                "subscription": False,
                "show_hero_banner": False,
            }

            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in SubscriptionBookReadView: {e}")
            messages.error(request, "Unable to load SubscriptionBookReadView!")
            return redirect("home:my_subscription_book_list")


@login_required
def book_pdf_view(request, book_id):
    user_book = UserSubscriptionBooks.objects.filter(
        book__id=book_id, user_subscription__user=request.user, user_subscription__active_status="active"
    ).first()
    # get_object_or_404(UserSubscriptionBooks, book=book_id, subscription__user=request.user)

    response = FileResponse(user_book.book.digital_file.open(), content_type="application/pdf")

    response["Content-Disposition"] = "inline"
    response["X-Frame-Options"] = "SAMEORIGIN"
    response["Cache-Control"] = "no-store"

    return response
