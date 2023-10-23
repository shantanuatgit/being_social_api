"""
URL configuration for being_social_api project.

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
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="being_social_api",
        default_version='v1',
        description="Being Social API is for Create, Read, Update and Destroy Post, Follow Unfollow users and Visit Profile.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('accounts/', include('profiles_api.urls')),
        path('posts/', include('pic_board.urls')),
        path('__debug__/', include(debug_toolbar.urls)),
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#         # ...
#     ]