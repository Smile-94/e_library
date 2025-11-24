from django.urls import path

# import views
from apps.account.views.login_view import SignUpView, UserLoginView, UserLogout

app_name = "account"
# <<------------------------------------*** Signup  URL ***------------------------------------>>
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
]
