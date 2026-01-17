# apps/book/urls.py
from django.urls import path

from apps.book.views.read_book import SubscriptionBookReadView

app_name = "book"

urlpatterns = [
    path("read/<int:book_id>/", SubscriptionBookReadView.as_view(), name="book_read"),
]
