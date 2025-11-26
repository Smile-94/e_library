from django.urls import path

# Views
from apps.authority.views.authority_home import AdminDashboardView
from apps.authority.views.user_management import UserListView

app_name = "authority"

# Dashboard Urls
urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]

# User Management Urls
urlpatterns += [
    path("user-list/", UserListView.as_view(), name="user_list"),
]
