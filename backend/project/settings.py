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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent
LIB_DIR = BASE_DIR / "lib"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "3v^zqg1nn+qhr%_8tcm9fw*t&19+2n_@1z93j57vo@ln)sp(ig"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    "rest_framework",
    "simple_history",
    "django_filters",
    "django_common_utils.apps.Config",
    "django_bleach",
    "private_storage",
    
    "apps.relation_managers.apps.RelationManagersConfig",
    
    "apps.authentication",
    "apps.lesson",
    "apps.event",
    "apps.homework",
    "apps.timetable",
    
    "apps.news",
    "apps.main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "simple_history.middleware.HistoryRequestMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/second",
        "user": "60/second"
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_PERMISSION_CLASSES": [
        "apps.utils.permissions.AuthenticationAndActivePermission"
    ]
}

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
                "apps.main.context_processors.constants_processor"
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

APPEND_SLASH = True

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "CET"

USE_I18N = False
USE_L10N = False
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = LIB_DIR / "MEDIA"

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

# EMAIL
DEFAULT_FROM_EMAIL = "testfrom@gmail.com"
SERVER_EMAIL = "test@gmail.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_SUBJECT_PREFIX = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_PASSWORD = None
EMAIL_HOST_USER = None

# Private storage
PRIVATE_STORAGE_PATH = LIB_DIR / "private_media"
