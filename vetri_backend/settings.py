import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
ENV = os.getenv("ENV", "production")  # can keep for toggling other configs

# -------------------------------
# SECURITY
# -------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET", "dev-fallback-secret")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ["true", "1", "yes"]
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# -------------------------------
# INSTALLED APPS
# -------------------------------
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Third-party
    'rest_framework',
    'corsheaders',
    'channels',

    # Local apps
    'app',
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
# URLS / TEMPLATES / WSGI / ASGI
# -------------------------------
ROOT_URLCONF = "vetri_backend.urls"

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

WSGI_APPLICATION = "vetri_backend.wsgi.application"
ASGI_APPLICATION = "vetri_backend.asgi.application"

# -------------------------------
# DATABASE (SQLite3 only)
# -------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -------------------------------
# CHANNELS
# -------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# -------------------------------
# REST FRAMEWORK + JWT
# -------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# -------------------------------
# CORS / CSRF
# -------------------------------
FRONTEND_URLS = os.getenv("FRONTEND_URLS", "https://vf-frontend.onrender.com").split(",")
FRONTEND_URLS = [url.strip().rstrip("/") for url in FRONTEND_URLS]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = FRONTEND_URLS
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = FRONTEND_URLS

APPEND_SLASH = True

# -------------------------------
# EMAIL SETTINGS
# -------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv("EMAIL_USER", "akila271819@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "ngyj hove cjsc penw")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -------------------------------
# STATIC FILES
# -------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# -------------------------------
# TIMEZONE / LOCALE
# -------------------------------
TIME_ZONE = "Asia/Kolkata"
USE_TZ = True
LANGUAGE_CODE = "en-us"

# -------------------------------
# DEFAULT PRIMARY KEY FIELD
# -------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
