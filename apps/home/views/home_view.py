import logging

from django.contrib import messages

# Permission and Authentication
# Django Response Class
from django.http import HttpResponse

# Django View Classes
from django.views import View

# Custom Permission Class

logger = logging.getLogger(__name__)


class HomeView(View):
    # template_name = "dashboard.html"  # your template path
    # user_model = User

    def get(self, request):
        try:
            # total_customer = self.user_model.objects.filter(is_staff=False).count()
            # total_staff = self.user_model.objects.filter(is_staff=True).count()
            # context = {"title": "Dashboard", "total_customer": total_customer, "total_staff": total_staff, "name": "Sazzad"}

            # return render(request, self.template_name, context)
            return HttpResponse("<h2>Working on Home View Design</h2>")

        except Exception as e:
            logger.exception(f"ERROR:------>> Error occurred in Admin Dashboard View: {e}")
            messages.error(request, "Unable to load dashboard!")
            return HttpResponse("Something went wrong!")
