from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="APIs",
      default_version='v1',
      description="Pulling results from openAI, this  endoints are designed to serve as a digital steward for families \
                seeking to nurture their faith and strengthen family bonds through daily devotions\
                 and guidance. It aims to provide a foundation of spiritual growth, moral integrity, and generational\
                blessings, inspired by the teachings found throughout the Bible",
      terms_of_service="https://www.codewithflex.com/policies/terms/",
      contact=openapi.Contact(email="codewithfelx@codewithflex.com"),
      license=openapi.License(name="License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include("endpoints.urls")),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]