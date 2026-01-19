import logging

from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import Random

# Permission and Authentication
# Django Response Class
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Django View Classes
from django.views import View

from apps.book.models.book_model import Book
from apps.book.models.category_model import Category
from apps.subscription.models.subscription_model import Subscription

# Custom Permission Class

logger = logging.getLogger(__name__)


# <<------------------------------------*** Home View ***------------------------------------>>
class HomeView(View):
    template_name = "index.html"  # your template path
    # user_model = User

    def get(self, request):
        try:
            # total_customer = self.user_model.objects.filter(is_staff=False).count()
            # total_staff = self.user_model.objects.filter(is_staff=True).count()
            all_categories = Category.objects.all()
            context = {
                "title": "Home",
                "all_categories": all_categories[:8],
                "history": Book.objects.filter(category__category_name="History").order_by("id").first(),
                "fiction_books": Book.objects.filter(title__icontains="The English Patient").order_by("id").first(),
                "programming_books": Book.objects.filter(category__category_name="Programming").order_by("id").first(),
                "programming_books_2": Book.objects.filter(title__icontains="হাতেকলমে জাভাস্ক্রিপ্ট").order_by("id").first(),
                "politics_books": Book.objects.filter(title__icontains="Not all springs end winter").order_by("id").first(),
                "rabindranath_tagore_books": Book.objects.filter(title__icontains="শেষের কবিতা").order_by("id").first(),
                "history_2": Book.objects.filter(title__icontains="অটুট পাথর").order_by("id").first(),
                "history_3": Book.objects.filter(title__icontains="উসমানি সালতানাতের ইতিহাস").order_by("id").first(),
                "latest_books": Book.objects.all().order_by("-id"),
                "categories": Category.objects.order_by(Random())[:10],
                "show_hero_banner": True,
                "hero_normal": "",
                "subscription": False,
            }

            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load Home Page!")
            return HttpResponse("Something went wrong!")


# <<------------------------------------*** Book Details View ***------------------------------------>>
class BookDetailsView(View):
    template_name = "book_details.html"  # your template path
    model_class = Book

    def get(self, request, pk):
        try:
            book = self.model_class.objects.filter(pk=pk).first()
            if not book:
                messages.error(request, "Book not found!")
                return redirect("home:index")

            context = {
                "title": "Book Details",
                "related_books": self.model_class.objects.filter(category=book.category).order_by(Random())[:4],
                "book_obj": book,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
                "show_hero_banner": False,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load book details!")
            return HttpResponse("Something went wrong!")


# <<------------------------------------*** Shope View ***------------------------------------>>
class ShopeView(View):
    template_name = "shope.html"  # your template path
    model_class = Book

    def get(self, request):
        try:
            books = self.model_class.objects.all().order_by("-id")
            context = {
                "title": "Shope",
                "books": books,
                "all_categories": Category.objects.all().annotate(count_book=Count("books_category")).order_by("-count_book"),
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "sale_off": books.filter(active_status="active").order_by("id")[:6],
                "subscription": False,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load Shop Page!")
            return HttpResponse("Something went wrong!")


class CategoryProductView(View):
    template_name = "category_product.html"  # your template path
    model_class = Book

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            books = self.model_class.objects.filter(category=category).order_by("id")
            context = {
                "title": "Shope",
                "books": books,
                "category": category,
                "all_categories": Category.objects.annotate(book_count=Count("books_category")).order_by("-book_count"),
                "show_hero_banner": False,
                "hero_normal": "hero-normal",
                "sale_off": books.filter(active_status="active").order_by("id")[:6],
                "subscription": False,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load Subscription Page!")
            return HttpResponse("Something went wrong!")


# <<------------------------------------*** Subscription View ***------------------------------------>>
class SubscriptionView(View):
    template_name = "subscription.html"  # your template path
    model_class = Subscription

    def get(self, request):
        try:
            all_categories = Category.objects.all()
            context = {
                "title": "Subscription",
                "subscription": True,
                "show_hero_banner": False,
                "all_categories": all_categories[:8],
                "hero_normal": "hero-normal",
                "subscriptions": self.model_class.objects.filter(active_status="active").order_by("id"),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load Subscription Page!")
            return HttpResponse("Something went wrong!")
