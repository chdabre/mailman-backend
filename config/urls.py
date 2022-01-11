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

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
