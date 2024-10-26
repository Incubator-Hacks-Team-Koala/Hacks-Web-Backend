"""
URL configuration for hacks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
# from reviews.views import ProductViewSet, ImageViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from team.views import TeamCreateListView

# router = DefaultRouter()
# router.register(r'team', TeamEditView.as_view(), basename='team_edit')
# router.register(r'image', ImageViewSet, basename='Image')

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/auth/', include('auth.urls')),
    path('api/teams/', include('team.urls')),
    path('api/hacks/', include('hackathon.urls')),
    path('api/user/', include('user.urls')),
    # path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)