from django.urls import path

# Views
from apps.authority.views.authority_home import AdminDashboardView
from apps.authority.views.user_management import UserListView
from apps.authority.views.manage_staff import (
    StaffUserListView,
    StaffUserEditView,
    StaffUserSoftDeleteView,
    StaffUserCreateView,
    StaffUserDetailView,
)

app_name = "authority"

# Dashboard Urls
urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]

# User Management Urls
urlpatterns += [
    path("user-list/", UserListView.as_view(), name="user_list"),
]

# Staff Management Urls
urlpatterns += [
    path("staff-create/", StaffUserCreateView.as_view(), name="staff_create"),
    path("staff-list/", StaffUserListView.as_view(), name="staff_list"),
    path("staff-edit/<int:pk>/", StaffUserEditView.as_view(), name="staff_edit"),
    path("staff-detail/<int:pk>/", StaffUserDetailView.as_view(), name="staff_detail"),
    path("staff-delete/<int:pk>/", StaffUserSoftDeleteView.as_view(), name="staff_delete"),
]
