from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import authentication 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(openapi.Info(
    title='Swagger using',
    default_version='v1',
    description='Just learning swagger for 1st time',
    contact = openapi.Contact(email='harshsahu709@gmail.com')
),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/blog/',include('blogs.urls')),
    path('api/auth/',include('authentication.urls')),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
