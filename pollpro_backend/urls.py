# pollpro_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

swagger_info = openapi.Info(
    title="PollPro API",
    default_version='v1',
    description="API for managing polls, votes, and admin tasks",
    terms_of_service="https://www.example.com/terms/",
    contact=openapi.Contact(email="contact@example.com"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/polls/', include('polls.urls')),
    path('api/admin/', include('pollpro_admin.urls')),
    path('api/users/', include('users.urls')), 
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]