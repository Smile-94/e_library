from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

# <<------------------------------------*** URLs ***------------------------------------>>
from apps.account import urls as account_urls
from apps.authority import urls as authority_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(account_urls)),
    path("", include(authority_urls)),
]
# for serve static files
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
