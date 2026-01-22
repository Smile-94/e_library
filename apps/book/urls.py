# apps/book/urls.py
from django.urls import path

from apps.book.views.read_book import SubscriptionBookReadView, book_pdf_view, SubscriptionBookDownloadView
from apps.book.views.download_payment import (
    InitiateBookPaymentView,
    BookPaymentSuccessView,
    BookPaymentFailView,
    BookPaymentCancelView,
)

app_name = "book"

urlpatterns = [
    path("read/<int:book_id>/", SubscriptionBookReadView.as_view(), name="book_read"),
    path("pdf/<int:book_id>/", book_pdf_view, name="book_pdf_view"),
    path("download/<int:book_id>/", SubscriptionBookDownloadView.as_view(), name="book_download"),
]

# <<------------------------------------*** Book Download Payment View ***------------------------------------>>
urlpatterns += [
    path("initiate-book-payment/<int:sub_book_id>/", InitiateBookPaymentView.as_view(), name="initiate_book_payment"),
    path("book-payment-success/", BookPaymentSuccessView.as_view(), name="book_payment_success"),
    path("book-payment-fail/", BookPaymentFailView.as_view(), name="book_payment_fail"),
    path("book-payment-cancel/", BookPaymentCancelView.as_view(), name="book_payment_cancel"),
]
