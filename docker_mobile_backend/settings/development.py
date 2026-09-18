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

if os.getenv("DATABASE_URL"):
    from urllib.parse import unquote, urlparse

    database_url = urlparse(os.getenv("DATABASE_URL"))

    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": database_url.path.lstrip("/"),
        "USER": database_url.username,
        "PASSWORD": unquote(database_url.password or ""),
        "HOST": database_url.hostname,
        "PORT": database_url.port or 5432,
    }
else:
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
