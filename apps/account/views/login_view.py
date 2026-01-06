import logging

from django.contrib import messages

# Permission and Authentication
from django.contrib.auth import authenticate, login, logout

# forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# class based view builtin class
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views import View

from apps.account.forms.account_forms import SignUpForm

# Models
from apps.account.models.user_model import User

logger = logging.getLogger(__name__)


# <<------------------------------------*** Signup  View ***------------------------------------>>
class SignUpView(View):
    template_name = "signup.html"

    def get(self, request):
        try:
            form = SignUpForm()
            return render(request, self.template_name, {"form": form, "title": "Sign Up"})
        except Exception as e:
            logger.exception(f"ERROR:--------------------> {e}")
            return HttpResponse("Something went wrong!")

    def post(self, request):
        try:
            form = SignUpForm(request.POST, request.FILES)  # include FILES for profile_photo
            if form.is_valid():
                form.save()
                messages.success(request, "Account created successfully!")
                return HttpResponseRedirect(reverse("account:login"))
            else:
                logger.error(f"WARNING:--------------------> {form.errors}")
                messages.error(request, "Please correct the errors below.")
                return render(request, self.template_name, {"form": form, "title": "Sign Up"})

        except Exception as e:
            logger.exception(f"ERROR:--------------------> SignUp View Error: {e}")
            return HttpResponse("Something went wrong!")


# <<------------------------------------*** Login  View ***------------------------------------>>
class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login Page"
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST["username"]
        password = self.request.POST["password"]

        try:
            request_user = User.objects.get(username=username)
            user = authenticate(self.request, username=username, password=password)

            if user is not None and request_user.is_staff is True:
                login(self.request, user)
                return HttpResponseRedirect(reverse("authority:admin_dashboard"))

            elif user is not None and request_user.is_active is True:
                login(self.request, user)
                return HttpResponseRedirect(reverse("home:home"))
                # return HttpResponse("Login Successful! we are working on home view")

            else:
                if User.objects.filter(username=username).exists() and request_user.is_active is False:
                    messages.warning(self.request, f"{username} this email don't have login permission")

                return HttpResponseRedirect(reverse("account:login"))

        except Exception as e:
            logger.exception(f"ERROR:-------------------->Login View Error: {e}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        logger.error(f"WARNING:--------------------> {form.errors}")
        messages.error(self.request, "Invalid User email password")
        return super().form_invalid(form)


# <<------------------------------------*** Logout  View ***------------------------------------>>
class UserLogout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                is_staff = request.user.is_staff
                logout(request)
                if is_staff:
                    # Staff user redirected to login
                    return HttpResponseRedirect(reverse("account:login"))
                else:
                    # Non-staff redirected to home
                    # return HttpResponseRedirect(reverse("home:home"))
                    return HttpResponse("You have been logged out!")
            return HttpResponseRedirect(reverse("account:login"))
        except Exception as e:
            logger.exception(f"ERROR:--------------------> Logout View Error: {e}")
            return HttpResponse("Something went wrong!")
