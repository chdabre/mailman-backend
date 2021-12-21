from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
   path('auth/', include('rest_auth.urls')),
   path('auth/registration/', include('rest_auth.registration.urls')),
   path('users/', include('users.urls')),
   path('', include('postcards.urls')),
   path('', include('jobs.urls')),
]

# Swagger / drf-yasg configuration

schema_view = get_schema_view(
   openapi.Info(
      title="Mailman API",
      default_version='v1',
      description="OpenAPI specification for Mailman API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]