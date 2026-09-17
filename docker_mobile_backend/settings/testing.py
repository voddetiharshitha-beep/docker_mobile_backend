from .base import *


# ============================================================
# TESTING
# ============================================================

DEBUG = False


# ============================================================
# TEST DATABASE
# ============================================================

DATABASES["default"].update({
    "NAME": os.getenv("TEST_POSTGRES_DB", "test_docker_backend"),
})


# ============================================================
# TEST EMAIL
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


# ============================================================
# TEST STORAGE
# ============================================================

DEFAULT_FILE_STORAGE = (
    "django.core.files.storage.InMemoryStorage"
)