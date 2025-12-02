import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# 🔐 SECURITY
# ==========================
SECRET_KEY = os.getenv("DJANGO_SECRET", "dev-secret")
DEBUG = True
ALLOWED_HOSTS = ["*"]


# ==========================
# 📦 INSTALLED APPS
# ==========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "channels",           # ✅ REQUIRED for WebSockets

    # Local apps
    "app",
    "chat",
]


# ==========================
# 🔧 MIDDLEWARE
# ==========================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================
# 🌐 URL / TEMPLATE
# ==========================
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
                "django.template.context_processors.csrf",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "vetri_backend.wsgi.application"


# ==========================
# 🗄 DATABASE
# ==========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==========================
# ⚡ ASGI / CHANNELS
# ==========================
ASGI_APPLICATION = "vetri_backend.asgi.application"   # ✅ FIXED

# In-memory channel layer for development
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


# ==========================
# 🔐 REST FRAMEWORK
# ==========================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
}


# ==========================
# 🌍 CORS
# ==========================
CORS_ALLOW_ALL_ORIGINS = True  # OK for dev, NOT for prod


# ==========================
# 📁 STATIC FILES
# ==========================
STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
