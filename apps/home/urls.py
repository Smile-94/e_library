from django.urls import path

from apps.home.views.home_view import (
    BookDetailsView,
    CategoryProductView,
    HomeView,
    ShopeView,
    SubscriptionView,
)
from apps.home.views.user_profile import EditMyProfileView, MyProfileView
from apps.home.views.user_subscription import AddBookToMySubscriptionView, MySubscriptionBookListView, MySubscriptionHistoryView

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("book-details/<int:pk>/", BookDetailsView.as_view(), name="home_book_details"),
    path("shope/", ShopeView.as_view(), name="home_shope"),
    path("shope/<int:pk>/", CategoryProductView.as_view(), name="home_shope_category"),
    path("subscription/", SubscriptionView.as_view(), name="home_subscription"),
    path("my-subscription-history/", MySubscriptionHistoryView.as_view(), name="my_subscription_history"),
    path("my-profile/", MyProfileView.as_view(), name="my_profile"),
    path("my-profile/edit/", EditMyProfileView.as_view(), name="edit_my_profile"),
    path("subscription/add-book/", AddBookToMySubscriptionView.as_view(), name="add_book_to_subscription"),
    path("my-subscription-book-list/", MySubscriptionBookListView.as_view(), name="my_subscription_book_list"),
]
