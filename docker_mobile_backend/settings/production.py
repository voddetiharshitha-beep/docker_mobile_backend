import os
from datetime import timedelta

from .base import *

# ============================================================
# PRODUCTION
# ============================================================

DEBUG = False


# ============================================================
# SECRET KEY
# ============================================================

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]


# ============================================================
# DATABASE
# ============================================================

DATABASES["default"].update({
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ["POSTGRES_DB"],
    "USER": os.environ["POSTGRES_USER"],
    "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "HOST": os.environ["POSTGRES_HOST"],
    "PORT": os.environ.get("POSTGRES_PORT", "5432"),
})


# ============================================================
# REDIS
# ============================================================

REDIS_URL = os.environ["REDIS_URL"]

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]

CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]


# ============================================================
# JWT
# ============================================================

SIMPLE_JWT.update({
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
})


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ["EMAIL_HOST"]

EMAIL_PORT = int(
    os.environ.get("EMAIL_PORT", "587")
)

EMAIL_USE_TLS = (
    os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"
)

EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]

EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# CORS
# ============================================================

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CORS_ALLOWED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = True


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]


# ============================================================
# HTTPS / SSL SECURITY
# ============================================================

SECURE_SSL_REDIRECT = True

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)


# ============================================================
# SECURE COOKIES
# ============================================================

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"


# ============================================================
# HSTS
# ============================================================

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


# ============================================================
# SECURITY HEADERS
# ============================================================

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_REFERRER_POLICY = "same-origin"


# ============================================================
# BROWSER SECURITY
# ============================================================

SECURE_BROWSER_XSS_FILTER = True
