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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.http import HttpResponse
from django.core.management import call_command


def update_event_statuses(request):
    """View to manually trigger event status updates"""
    count = call_command('update_event_statuses')
    return HttpResponse(f"Updated {count} event statuses")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='home'),
    path('user/', include('user.urls')),
    path('badge/', include('badge.urls')),
    path('event/', include('event.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('notification/', include('notification.urls')),
    path('review/', include('review.urls')),
    path('admin/update-event-statuses/', update_event_statuses, name='update_event_statuses'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)