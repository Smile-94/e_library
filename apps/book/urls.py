# apps/book/urls.py
from django.urls import path

from apps.book.views.read_book import SubscriptionBookReadView, book_pdf_view

app_name = "book"

urlpatterns = [
    path("read/<int:book_id>/", SubscriptionBookReadView.as_view(), name="book_read"),
    path("pdf/<int:book_id>/", book_pdf_view, name="book_pdf_view"),
]
