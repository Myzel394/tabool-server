"""
Django settings for backend project.

Generated by "django-admin startproject" using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

from django.db.models import CharField
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

CharField.register_lookup(Lower)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent
LIB_DIR = BASE_DIR / "lib"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", 1))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(" ")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    
    "rest_framework",
    "simple_history",
    "django_filters",
    "django_common_utils.apps.Config",
    "django_bleach",
    "private_storage",
    "simple_email_confirmation",
    "channels",
    "django_eventstream",
    "django_crontab",
    "django_object_actions",
    "corsheaders",
    
    "apps.django.utils.relation_managers.apps.RelationManagersConfig",
    
    "apps.django.main.authentication",
    "apps.django.main.school_data",
    "apps.django.main.lesson",
    "apps.django.main.event",
    "apps.django.main.homework",
    "apps.django.main.otp",
    
    "apps.django.extra.scooso_scraper",
    "apps.django.extra.news",
    
    "apps.django.core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_grip.GripMiddleware",
    "apps.django.utils.middleware.RequestPreferredIdMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.getenv("THROTTLE_ANON"),
        "user": os.getenv("THROTTLE_USER"),
        "autocomplete": os.getenv("THROTTLE_AUTOCOMPLETE"),
    },
    "DEFAULT_PAGINATION_CLASS": "apps.django.utils.paginations.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("DEFAULT_PAGE_SIZE")),
    "DEFAULT_PERMISSION_CLASSES": [
        "apps.django.utils.permissions.AuthenticationAndActivePermission",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "apps.django.utils.permissions.unauthorized_handler"
}

CRONJOBS = [
    (os.getenv("CRON_FETCH_TIMETABLE_DAY"), "apps.django.main.lesson.cron_jobs.fetch_timetable_from_users"),
    (os.getenv("CRON_FETCH_TIMETABLE_NIGHT"), "apps.django.main.lesson.cron_jobs.fetch_timetable_from_users"),
    (os.getenv("CRON_FETCH_TIMETABLE_DAY_WEEKEND"), "apps.django.main.lesson.cron_jobs.fetch_timetable_from_users"),
    (os.getenv("CRON_FETCH_TIMETABLE_NIGHT_WEEKEND"), "apps.django.main.lesson.cron_jobs.fetch_timetable_from_users"),
    (os.getenv("CRON_FETCH_USER_NAMES"), "apps.django.main.authentication.cron_jobs.fetch_user_names"),
    (os.getenv("CRON_CLEANUP_LIB_FOLDER"), "apps.django.core.cron_jobs.cleanup_lib_dir")
]

AUTH_USER_MODEL = "authentication.User"

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / ".." / "frontend" / "public"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"
ASGI_APPLICATION = "project.routing.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": os.getenv("POSTGRES_DB", "tabool_django_database"),
        "USER": os.getenv("POSTGRES_USER", "tabool_django_role"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432")
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        'NAME': 'pwned_passwords_django.validators.PwnedPasswordsValidator',
        'OPTIONS': {
            'error_message': _("Dieses Passwort wurde bereits schon mal gehackt! Das Passwort muss einzigartig sein."),
            'help_message': _("Dein Passwort muss einzigartig sein."),
        }
    },
]

APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "CET"

USE_I18N = True
USE_L10N = False
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_root"

MEDIA_ROOT = LIB_DIR / "media"
MEDIA_URL = "/media/"

SIMPLE_HISTORY_HISTORY_ID_USE_UUID = True
SIMPLE_HISTORY_FILEFIELD_TO_CHARFIELD = True
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True


def create_around_style(prefix: str, arounds=None):
    arounds = arounds or ["top", "right", "bottom", "left"]
    for around in arounds:
        yield f"{prefix}-{around}"


BLEACH_ALLOWED_TAGS = [
    *(f"h{i}" for i in range(1, 6 + 1)),
    "p",
    "i", "em",
    "b", "strong",
    "a",
    "ul", "ol", "li",
    "blockquote",
    "hr", "br",
    "img",
    "div",
    "br",
    "table", "tr", "th", "td", "thead", "tbody",
    "dl", "dt", "dd"
]
BLEACH_ALLOWED_ATTRIBUTES = [
    "href",
    "title",
    "style",
    "src", "loading", "width", "height", "alt"
]
BLEACH_ALLOWED_STYLES = [
    "margin", *(create_around_style("margin-")),
    "padding", *(create_around_style("padding-")),
    "color",
    "text-align", "text-decoration"
]
BLEACH_ALLOWED_PROTOCOLS = [
    "https", "data"
]
BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True

# SESSION & LOGIN
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days

# EMAIL
DEFAULT_FROM_EMAIL = "testfrom@gmail.com"
SERVER_EMAIL = "test@gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

SIMPLE_EMAIL_CONFIRMATION_KEY_LENGTH = 40

EMAIL_MAIL_HTML = "authentication/emails/confirm.html"
EMAIL_MAIL_PLAIN = "authentication/emails/confirm.txt"
EMAIL_PAGE_TEMPLATE = "authentication/email_confirmation.html"

# Private storage
PRIVATE_STORAGE_FOLDER = "private"
PUBLIC_STORAGE_FOLDER = "public"
PRIVATE_STORAGE_PATH = LIB_DIR / PRIVATE_STORAGE_FOLDER
PRIVATE_STORAGE_AUTH_FUNCTION = "apps.django.utils.private_storages.private_storage_access_check"

# Event stream
EVENTSTREAM_STORAGE_CLASS = "django_eventstream.storage.DjangoModelStorage"
EVENTSTREAM_CHANNELMANAGER_CLASS = "apps.django.utils.permissions.UserActiveChannelManager"

MAX_UPLOAD_SIZE = 5242880  # 50MB

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    ALLOWED_HOSTS = ["*"]

SESSION_COOKIE_HTTPONLY = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = ""

CREATE_USERS_IN_THREAD = False
