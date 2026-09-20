from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "success",
        "message": "Django backend is running",
    })


def database_health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return JsonResponse({
            "status": "healthy",
            "service": "database",
        })
    except Exception:
        return JsonResponse(
            {
                "status": "unhealthy",
                "service": "database",
            },
            status=503,
        )


def redis_health_check(request):
    try:
        cache.set("health_check", "ok", timeout=30)
        result = cache.get("health_check")

        if result != "ok":
            raise RuntimeError("Redis health check failed")

        return JsonResponse({
            "status": "healthy",
            "service": "redis",
        })
    except Exception:
        return JsonResponse(
            {
                "status": "unhealthy",
                "service": "redis",
            },
            status=503,
        )