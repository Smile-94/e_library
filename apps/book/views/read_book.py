import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.views import View
from apps.book.models import Book
from apps.subscription.models.user_subscription_model import UserSubscriptionBooks
from apps.subscription.utils import get_active_subscription
from django.http import JsonResponse, FileResponse
from apps.subscription.models.subscription_model import SubscriptionDownloadChoices

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


# <<------------------------------------*** Download Book View ***------------------------------------>>
class SubscriptionBookDownloadView(LoginRequiredMixin, View):
    model_class = Book
    user_subscription_book = UserSubscriptionBooks

    def get(self, request, book_id):
        try:
            if request.headers.get("X-Requested-With") != "XMLHttpRequest":
                return JsonResponse({"message": "Invalid request"}, status=400)

            book = self.model_class.objects.filter(id=book_id).first()
            if not book or not book.digital_file:
                return JsonResponse({"message": "Book does not have a downloadable file"}, status=400)

            subscription = get_active_subscription(request.user)
            if not subscription:
                return JsonResponse({"message": "No active subscription found"}, status=403)

            sub_book = self.user_subscription_book.objects.filter(user_subscription=subscription, book=book).first()

            if not sub_book:
                return JsonResponse({"message": "Book not added to subscription"}, status=403)

            if sub_book.download_count == 0:
                if subscription.subscription.book_download_limit == SubscriptionDownloadChoices.LIMITED:
                    MAX_DOWNLOAD = subscription.subscription.max_book_download_limit

                    if MAX_DOWNLOAD and subscription.download_count >= MAX_DOWNLOAD:
                        return JsonResponse({"message": "Download limit exceeded"}, status=403)

                # First-time download → count it
                subscription.download_count += 1
                subscription.save(update_fields=["download_count"])

                sub_book.download_count = 1
                sub_book.save(update_fields=["download_count"])

            # if subscription.subscription.book_download_limit == SubscriptionDownloadChoices.LIMITED:
            #     MAX_DOWNLOAD = subscription.subscription.max_book_download_limit
            #     if MAX_DOWNLOAD and subscription.download_count >= MAX_DOWNLOAD:
            #         return JsonResponse({"message": "Download limit exceeded"}, status=403)

            # # Prevent Multiple Count for Same Book
            # if sub_book.download_count == 0:
            #     subscription.download_count += 1
            #     subscription.save(update_fields=["download_count"])

            #     sub_book.download_count = 1
            #     sub_book.save(update_fields=["download_count"])

            return FileResponse(
                book.digital_file.open("rb"),
                as_attachment=True,
                filename=f"{book.title}.pdf",
            )

        except Exception as e:
            logger.exception(f"ERROR:------>> SubscriptionBookDownloadView: {e}")
            return JsonResponse({"message": "Unable to download book"}, status=500)
