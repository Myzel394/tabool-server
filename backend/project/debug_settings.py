# noinspection PyUnresolvedReferences
from .base_settings import *

DEBUG = True

SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ["*"]
