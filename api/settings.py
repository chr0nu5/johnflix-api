import os
import sys

from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', "random")
DEBUG = os.environ.get('DEBUG', False)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = INSTALLED_APPS + [
    'content',
    'rest',

    'rest_framework',
    'rest_framework.authtoken',

    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 40,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['default']['NAME'] = 'test'

if os.environ.get("REMOTE_DB_HOST", None):
    DATABASES['remote'] = {}
    DATABASES['remote']['ENGINE'] = 'django.db.backends.sqlite3'
    DATABASES['remote']['HOST'] = os.environ.get("HOST")
    DATABASES['remote']['NAME'] = os.environ.get("NAME")
    DATABASES['remote']['USER'] = os.environ.get("USER")
    DATABASES['remote']['PASSWORD'] = os.environ.get("PASSWORD")


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilari'
        'tyValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidato'
        'r',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidat'
        'or',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValida'
        'tor',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FRONTEND_URL = os.getenv("FRONTEND_URL", ".")
DRF_TOKEN_TTL = 3600*24*365

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}

CACHE_TTL = os.getenv("CACHE_TTL", 3600)

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:8000")
]

JAZZMIN_SETTINGS = {
    "site_title": "FLIX",
    "show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-danger",
    "accent": "accent-danger",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "cerulean",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}
