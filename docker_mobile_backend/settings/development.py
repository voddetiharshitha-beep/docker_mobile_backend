from .base import *


# ============================================================
# DEVELOPMENT
# ============================================================

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]


# ============================================================
# DATABASE
# ============================================================

DATABASES["default"].update({
    "NAME": os.getenv("POSTGRES_DB", "docker_backend"),
    "USER": os.getenv("POSTGRES_USER", "docker_user"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD", "docker_password"),
    "HOST": os.getenv("POSTGRES_HOST", "postgres"),
    "PORT": os.getenv("POSTGRES_PORT", "5432"),
})


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ============================================================
# DEVELOPMENT STORAGE
# ============================================================

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"