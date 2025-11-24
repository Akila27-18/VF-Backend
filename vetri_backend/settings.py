import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# LOAD ENV
# --------------------------------------------------
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
ENV = os.getenv("ENV", "production")  # Production mode

# --------------------------------------------------
# SECURITY
# --------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET", "supersecret123")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ["true", "1", "yes"]
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "vf-backend-1.onrender.com").split(",")

# --------------------------------------------------
# INSTALLED APPS
# --------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",

    "rest_framework",
    "corsheaders",
    "channels",

    "app",
    "chat",
]

# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------
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

# --------------------------------------------------
# URLS / TEMPLATES / WSGI / ASGI
# --------------------------------------------------
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

# --------------------------------------------------
# DATABASE (SQLite for production)
# --------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------
# CHANNELS (Redis for production)
# --------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL", "redis://localhost:6379/0")],
        },
    }
}

# --------------------------------------------------
# REST FRAMEWORK + JWT
# --------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

# --------------------------------------------------
# CORS / CSRF
# --------------------------------------------------
FRONTEND_URLS = os.getenv("FRONTEND_URLS", "https://vf-frontend.onrender.com").split(",")
FRONTEND_URLS = [url.strip().rstrip("/") for url in FRONTEND_URLS]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = FRONTEND_URLS
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = FRONTEND_URLS

# --------------------------------------------------
# Trailing slash fix
# --------------------------------------------------
APPEND_SLASH = True

# --------------------------------------------------
# EMAIL SETTINGS
# --------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.getenv("EMAIL_USER", "akila271819@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "ngyj hove cjsc penw")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# --------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
