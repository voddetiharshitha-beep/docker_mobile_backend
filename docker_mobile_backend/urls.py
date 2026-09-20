"""
URL configuration for docker_mobile_backend project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import TaskListCreateView

from .views import (
    database_health_check,
    health_check,
    redis_health_check,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Health checks
    path("api/health/", health_check, name="health-check"),
    path(
        "api/health/database/",
        database_health_check,
        name="database-health-check",
    ),
    path(
        "api/health/redis/",
        redis_health_check,
        name="redis-health-check",
    ),

    # JWT authentication
    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),

    # Business API
    path(
        "api/tasks/",
        TaskListCreateView.as_view(),
        name="task-list-create",
    ),
]