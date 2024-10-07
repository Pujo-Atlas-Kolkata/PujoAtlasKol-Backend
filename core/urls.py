"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,  include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from user.views import LoginView, LogoutView, CustomTokenRefreshView  # Import the login and logout views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pujo/', include('pujo.urls')),
    path('user/', include('user.urls')),
    path('review/', include('reviews.urls')),
    path('login', LoginView.as_view(), name='login'),  # Direct login path
    path('logout', LogoutView.as_view(), name='logout'),  # Direct logout path
    path('api/token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # OpenAPI schema
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('metro/',include('metro.urls')),
    path("service/", include('service.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)