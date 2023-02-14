from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main_app.views import index, Search
from django.views.static import serve as mediaserve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls, name="admin-panel"),

    path("", index, name="home"),
    path("", include("blogs.urls")),
    path("", include("registration.urls")),
    path("", include("authors_profile.urls")),
    path("", include("main_app.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("il8n/", include("django.conf.urls.i18n")),
    path('search/', Search.as_view(), name="search"),
    path("", include("blogs.urls")),
    path("", include("authors_profile.urls")),
    path("", include("registration.urls")),
    path("", include("main_app.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
            re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
                mediaserve, {'document_root': settings.MEDIA_ROOT}),
            re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
                mediaserve, {'document_root': settings.STATIC_ROOT}),
            ]

handler404 = "cardioresp.views.handler404"
handler500 = 'cardioresp.views.handler500'
