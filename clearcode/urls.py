"""
    clearcode URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from apps.cart import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("items/", views.AddItemAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
