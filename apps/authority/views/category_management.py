import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from apps.book.filters.category_filter import CategorySearchFilter
from apps.book.forms.category_forms import CategoryForm
from apps.book.models.category_model import Category
from apps.common.permissions import RBACPermissionRequiredMixin, StaffPassesTestMixin

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** Category Create View ***------------------------------------>>
class CategoryCreateView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_add_book_category"
    template_name = "book_category_create.html"
    model_class = Category
    form_class = CategoryForm
    success_url = reverse_lazy("authority:book_category_list")

    def get(self, request):
        try:
            context = {
                "title": "Create Category",
                "form_title": "Create Category",
                "form": self.form_class(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Category Create GET View: {e}")
            messages.error(request, "Unable to load Category details!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                category = form.save()
                category.save()
                messages.success(request, "Category created successfully!")
                return redirect(self.success_url)

            context = {
                "title": "Create Category",
                "form_title": "Create Category",
                "form": form,
            }
            messages.error(request, "Unable to create Category!")
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Category Create POST View: {e}")
            messages.error(request, "Unable to create Category!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Category List View ***------------------------------------>>
class CategoryListView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_view_book_category"
    template_name = "book_category_list.html"
    model_class = Category
    filter_class = CategorySearchFilter

    def get(self, request):
        try:
            data_list = self.model_class.objects.all().order_by("id")

            context = {
                "title": "Category List",
                "table_title": "Category List",
                "data_list": self.filter_class(request.GET, queryset=data_list),
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Category List View: {e}")
            messages.error(request, "Unable to load Category list!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Category Edit View ***------------------------------------>>
class CategoryEditView(LoginRequiredMixin, RBACPermissionRequiredMixin, StaffPassesTestMixin, View):
    required_permission = "can_edit_book_category"
    template_name = "edit_book_category.html"
    model_class = Category
    form_class = CategoryForm

    def get(self, request, pk, *args, **kwargs):
        try:
            category = self.model_class.objects.filter(pk=pk).first()

            if not category:
                messages.error(request, "Category not found!")
                return redirect("authority:book_category_list")

            context = {
                "title": "Edit Category",
                "form_title": "Edit Category",
                "form": self.form_class(instance=category),
                "user_obj": category,
            }
            return render(request, self.template_name, context)

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Category Edit GET View: {e}")
            messages.error(request, "Unable to load Category details!")
            return HttpResponse(f"{e}")

    def post(self, request, pk):
        try:
            category = self.model_class.objects.filter(pk=pk).first()

            if not category:
                messages.error(request, "Category not found!")
                return redirect("authority:book_category_list")

            form = self.form_class(request.POST, request.FILES, instance=category)

            if not form.is_valid():
                context = {
                    "title": "Edit Category",
                    "form_title": "Edit Category",
                    "form": form,
                    "user_obj": category,
                }
                messages.error(request, "Unable to update Category!")
                return render(request, self.template_name, context)

            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("authority:book_category_list")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Category Edit POST View: {e}")
            messages.error(request, "Unable to update Category!")
            return HttpResponse(f"{e}")
