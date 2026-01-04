import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.account.forms.user_forms import EditMyProfileForm
from apps.book.models.category_model import Category

logger = logging.getLogger(__name__)
User = get_user_model()


# <<------------------------------------*** My Profile View ***------------------------------------>>
class MyProfileView(LoginRequiredMixin, View):
    template_name = "my_profile.html"
    model_class = User

    def get(self, request):
        try:
            user = self.model_class.objects.filter(pk=request.user.pk).first()
            context = {
                "title": "My Profile",
                "user": user,
                "show_hero_banner": False,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in My Profile View: {e}")
            messages.error(request, "Unable to load My Profile!")
            return HttpResponse(f"{e}")


# <<------------------------------------*** Edit My Profile View ***------------------------------------>>
class EditMyProfileView(LoginRequiredMixin, View):
    template_name = "edit_my_profile.html"
    model_class = User
    form_class = EditMyProfileForm

    def get(self, request):
        try:
            user = self.model_class.objects.filter(pk=request.user.pk).first()
            context = {
                "title": "Edit My Profile",
                "user": user,
                "form": self.form_class(instance=user),
                "show_hero_banner": False,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Edit My Profile View: {e}")
            messages.error(request, "Unable to load Edit My Profile!")
            return HttpResponse(f"{e}")

    def post(self, request):
        try:
            user = self.model_class.objects.filter(pk=request.user.pk).first()
            form = self.form_class(request.POST, request.FILES, instance=user)

            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("home:my_profile")

            context = {
                "title": "Edit My Profile",
                "user": user,
                "form": form,
                "show_hero_banner": False,
                "all_categories": Category.objects.all()[:8],
                "hero_normal": "hero-normal",
                "subscription": False,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Edit My Profile View: {e}")
            messages.error(request, "Unable to update Profile!")
            return HttpResponse(f"{e}")
