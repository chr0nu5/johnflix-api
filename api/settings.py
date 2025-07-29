import os
import sys

from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "random")
DEBUG = os.environ.get("DEBUG", False)
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = INSTALLED_APPS + [
    "content",
    "rest",

    "rest_framework",
    "rest_framework.authtoken",

    "django_filters",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS":
        "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 40,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

MIDDLEWARE = [
    "api.middleware.CorsMiddleware",
    "rest.middlewares.AllowOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "api.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
    }
}

if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"
    DATABASES["default"]["NAME"] = "test"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilari"
        "tyValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidato"
        "r",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidat"
        "or",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValida"
        "tor",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

FRONTEND_URL = os.getenv("FRONTEND_URL", ".")
DRF_TOKEN_TTL = 3600*24*365

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://{}:6379/1".format(os.environ.get("REDIS_HOST")),
    }
}

CACHE_TTL = os.getenv("CACHE_TTL", 3600)

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000")
]

UNFOLD = {
    "SITE_TITLE": "JohnFLIX",
    "SITE_HEADER": "JohnFLIX",
    "SITE_URL": "https://flix.john.dev.br",
    "SITE_LOGO": {
        "light": "https://flix.john.dev.br/img/icon.png",
        "dark": "https://flix.john.dev.br/img/icon.png",
    },
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "500": "255, 72, 36",
            "600": "255, 72, 36",
        },
    },
    "SITE_SYMBOL": "speed",
    "SIDEBAR": {
        "show_search": True,
    },
}
