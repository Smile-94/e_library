import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.book.filters.book_filter import BookSearchFilter
from apps.book.forms.book_forms import BookForm
from apps.book.models.book_model import Book
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** Book Create View ***------------------------------------>>
class BookCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_book"
    template_name = "book_create.html"
    model_class = Book
    form_class = BookForm
    success_url = reverse_lazy("authority:book_list")

    def get(self, request):
        try:
            context = {
                "title": "Create Book",
                "form_title": "Create Book",
                "form": self.form_class(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Book Create GET View: {e}")
            messages.error(request, "Unable to load Book details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                book = form.save()
                book.created_by = request.user
                book.save()
                messages.success(request, "Book created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Book",
                "form_title": "Create Book",
                "form": form,
            }
            messages.error(request, "Unable to create Book!")
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Book Create POST View: {e}")
            messages.error(request, "Unable to create Book!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Book Edit View ***------------------------------------>>
class BookEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_book"
    template_name = "edit_book.html"
    model_class = Book
    form_class = BookForm

    def get(self, request, pk, *args, **kwargs):
        try:
            book = self.model_class.objects.filter(pk=pk).first()
            if not book:
                messages.error(request, "Book not found!")
                return redirect("authority:book_list")

            context = {
                "title": "Edit Book",
                "form_title": "Edit Book",
                "form": self.form_class(instance=book),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Book Edit GET View: {e}")
            messages.error(request, "Unable to load Book details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            book = self.model_class.objects.filter(pk=pk).first()
            if not book:
                messages.error(request, "Book not found!")
                return redirect("authority:book_list")

            form = self.form_class(request.POST, request.FILES, instance=book)
            if not form.is_valid():
                context = {
                    "title": "Edit Book",
                    "form_title": "Edit Book",
                    "form": form,
                    "user_obj": book,
                }
                messages.error(request, "Unable to update Book!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect("authority:book_list")
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Book Edit POST View: {e}")
            messages.error(request, "Unable to update Book!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Book List View ***------------------------------------>>
class BookListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_book"
    template_name = "book_list.html"
    model_class = Book
    filter_class = BookSearchFilter

    def get(self, request):
        try:
            books = self.model_class.objects.all().order_by("id")

            context = {
                "title": "Book List",
                "table_title": "Book List",
                "books": self.filter_class(request.GET, queryset=books),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Book List View: {e}")
            messages.error(request, "Unable to load Book list!")
            return HttpResponse(f"{e}")


# <<
