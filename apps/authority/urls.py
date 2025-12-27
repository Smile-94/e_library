from django.urls import path

from apps.authority.views.author_management import (
    AuthorCreateView,
    AuthorDetailView,
    AuthorEditView,
    AuthorEducationCreateView,
    AuthorEducationEditView,
    AuthorListView,
    AuthorSoftDeleteView,
    AuthorWorkExperienceCreateView,
    AuthorWorkExperienceEditView,
)

# Views
from apps.authority.views.authority_home import AdminDashboardView
from apps.authority.views.book_management import (
    BookCreateView,
    BookEditView,
    BookListView,
)
from apps.authority.views.category_management import (
    CategoryCreateView,
    CategoryEditView,
    CategoryListView,
)
from apps.authority.views.manage_staff import (
    StaffUserCreateView,
    StaffUserDetailView,
    StaffUserEditView,
    StaffUserListView,
    StaffUserSoftDeleteView,
)
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

# Staff Management Urls
urlpatterns += [
    path("staff-create/", StaffUserCreateView.as_view(), name="staff_create"),
    path("staff-list/", StaffUserListView.as_view(), name="staff_list"),
    path("staff-edit/<int:pk>/", StaffUserEditView.as_view(), name="staff_edit"),
    path("staff-detail/<int:pk>/", StaffUserDetailView.as_view(), name="staff_detail"),
    path("staff-delete/<int:pk>/", StaffUserSoftDeleteView.as_view(), name="staff_delete"),
]

# Author Management Urls
urlpatterns += [
    path("author-create/", AuthorCreateView.as_view(), name="author_create"),
    path("author-list/", AuthorListView.as_view(), name="author_list"),
    path("author-edit/<int:pk>/", AuthorEditView.as_view(), name="author_edit"),
    path("author-detail/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
    path("author-delete/<int:pk>/", AuthorSoftDeleteView.as_view(), name="author_delete"),
    # Author Work Experience Urls
    path("author-experience-create/<int:pk>/", AuthorWorkExperienceCreateView.as_view(), name="author_experience_create"),
    path("author-experience-edit/<int:pk>/", AuthorWorkExperienceEditView.as_view(), name="author_experience_edit"),
    # Author Education Urls
    path("author-education-create/<int:pk>/", AuthorEducationCreateView.as_view(), name="author_education_create"),
    path("author-education-edit/<int:pk>/", AuthorEducationEditView.as_view(), name="author_education_edit"),
]

# Book Category Management Urls
urlpatterns += [
    path("book-category-list/", CategoryListView.as_view(), name="book_category_list"),
    path("book-category-create/", CategoryCreateView.as_view(), name="book_category_create"),
    path("book-category-edit/<int:pk>/", CategoryEditView.as_view(), name="book_category_edit"),
]

# Book Management Urls
urlpatterns += [
    path("book-create/", BookCreateView.as_view(), name="book_create"),
    path("book-list/", BookListView.as_view(), name="book_list"),
    path("book-edit/<int:pk>/", BookEditView.as_view(), name="book_edit"),
]
