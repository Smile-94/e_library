from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# <<------------------------------------*** URLs ***------------------------------------>>
from apps.account import urls as account_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(account_urls)),
]
# for serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
