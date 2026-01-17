from apps.book.models.category_model import Category


def all_categories(request):
    return {"all_categories": Category.objects.all()}
