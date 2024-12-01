import os
import sys
from pathlib import Path

TOKEN = "Bx66BEoL1JYSfD82ZwjdozyR5aW695XsYMHvwXZKXjkzs57IHZRiwdDI6Gi8qAbf"


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
SECRET_KEY = TOKEN
DEBUG = True
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'https://knigomania.qnro.ru']
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "semantic_admin",
    "django_filters",
    "semantic_forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.book",
    "apps.login",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
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
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test",  # Имя базы данных
        "USER": "test",  # Имя пользователя
        "PASSWORD": "test",  # Пароль пользователя
        "HOST": "192.168.1.234",  # Или 'db' если вы используете Docker Networking
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
AUTH_USER_MODEL = "login.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/login/"
