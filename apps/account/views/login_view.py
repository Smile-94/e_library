from django.shortcuts import HttpResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect

# Permission and Authentication
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin


# class based view builtin class
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import CreateView

# Models
from apps.account.models.user_model import User

# forms
from django.contrib.auth.forms import AuthenticationForm
from apps.account.forms.account_forms import SignUpForm


# <<------------------------------------*** Signup  View ***------------------------------------>>
class SignUpView(View):
    template_name = "signup.html"  # your template path

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form, "title": "Sign Up"})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES)  # include FILES for profile_photo
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            # return redirect("login")
            return HttpResponse("Account created successfully!")
        else:
            # Form is invalid; errors will be available in the template
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, {"form": form, "title": "Sign Up"})
