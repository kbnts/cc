"""
Settings for clearcode project.
"""
import os
from pathlib import Path

import environ

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# App config
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY", cast=str, default="BOLLOCKS BOLLOCKS")

CART_EXPIRES_AFTER_SECS = 72 * 60 * 60
CART_UUID_COOKIE_NAME = "c_id"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST", default="db"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f'redis://{env("REDIS_HOST")}:{env("REDIS_PORT")}',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

KAFKA_HOST = env("KAFKA_HOST")
KAFKA_PORT = env("KAFKA_PORT")
KAFKA_URL = f"{KAFKA_HOST}:{KAFKA_PORT}"
KAFKA_STREAM_TOPIC = "items"

CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "apps.cart",
    "apps.faustapp",
]

THIRD_PARTY_APPS = []

DEBUG_APPS = ["debug_toolbar"]

INSTALLED_APPS = CORE_APPS + PROJECT_APPS + THIRD_PARTY_APPS
if DEBUG:
    INSTALLED_APPS += DEBUG_APPS

CORE_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

APP_MIDDLEWARE = []
DEBUG_MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"]

MIDDLEWARE = CORE_MIDDLEWARE + APP_MIDDLEWARE
if DEBUG:
    MIDDLEWARE += DEBUG_MIDDLEWARE

ROOT_URLCONF = "clearcode.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "clearcode.wsgi.application"

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

# Core App config
ALLOWED_HOSTS = []
if DEBUG:
    ALLOWED_HOSTS = ["*"]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Misc
if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
