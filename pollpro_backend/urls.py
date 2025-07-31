# pollpro_backend/pollpro_backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Add admin URLs
    path('api/users/', include('users.urls')),
]