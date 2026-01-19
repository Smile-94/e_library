from django.db.models import Count

from apps.book.models.category_model import Category


def all_categories(request):
    return {"all_categories": Category.objects.annotate(book_count=Count("books_category")).order_by("-book_count")}
