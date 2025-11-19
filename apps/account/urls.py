from django.urls import path

# import views
from apps.account.views.login_view import SignUpView

# <<------------------------------------*** Signup  URL ***------------------------------------>>
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
