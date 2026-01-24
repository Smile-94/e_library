import logging

# Permission and Authentication
# Django Response Class
from django.shortcuts import render

# Django View Classes
from django.views import View

# Custom Permission Class

logger = logging.getLogger(__name__)


class NewPageView(View):
    template_name = "new_page.html"  # your template path

    def get(self, request):
        context = {"title": "New Page", "data": "Hello World"}
        return render(request, self.template_name, context)
