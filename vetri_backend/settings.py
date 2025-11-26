# vetri_backend/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
ENV = os.getenv("ENV", "production")

# -------------------------------
# SECURITY
# -------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET", "dev-fallback-secret")
DEBUG = ENV != "production"

ALLOWED_HOSTS = [
    "*",
    "vf-backend.onrender.com",
    "localhost",
    "127.0.0.1",
]

# -------------------------------
# INSTALLED APPS
# -------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "channels",
    "django_extensions",
    "rest_framework_simplejwt",

    # Local
    "app",
]

# -------------------------------
# MIDDLEWARE
# -------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------
# URLS / ASGI / WSGI
# -------------------------------
ROOT_URLCONF = "vetri_backend.urls"

WSGI_APPLICATION = "vetri_backend.wsgi.application"
ASGI_APPLICATION = "vetri_backend.asgi.application"

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

# -------------------------------
# DATABASE (SQLite)
# -------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------------------------------
# CHANNELS LAYER (REQUIRED for WebSockets)
# -------------------------------
REDIS_URL = os.getenv("REDIS_URL")  # Render Redis

if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
            },
        }
    }
else:
    # Local fallback
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }

# -------------------------------
# REST + JWT
# -------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

# -------------------------------
# CORS / CSRF
# -------------------------------
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "https://vf-backend.onrender.com",
    "https://vf-frontend.onrender.com",
    "http://localhost:5173",
]

CORS_ALLOW_HEADERS = ["*"]

# -------------------------------
# EMAIL SETTINGS
# -------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -------------------------------
# TIMEZONE & DEFAULTS
# -------------------------------
TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
LANGUAGE_CODE = "en-us"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True
