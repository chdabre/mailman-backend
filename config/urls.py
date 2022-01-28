from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

import website
from config import settings

urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
]


# Sentry test
def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns += [
    path('sentry-debug/', trigger_error),
]

# Serve media on debug server
if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
