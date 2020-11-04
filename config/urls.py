from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import api

# URLs that can be seen by Swagger after one has authenticated
public_apis = [
    path('api/v1/', include(api)),
]

# Remove docs from production
schema_view = get_schema_view(
    openapi.Info(
        title="RSS SCRAPER DOCS",
        default_version='v1',
        description="RSS SCRAPER APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="iamjackwachira@gmail.com"),
    ),
    permission_classes=(permissions.AllowAny,),
    public=True,
    patterns=public_apis,
)

docs = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=None),
         name='schema-swagger-ui')
]

urlpatterns = public_apis + docs + [
    path('admin/', admin.site.urls)
]


urlpatterns += staticfiles_urlpatterns()
