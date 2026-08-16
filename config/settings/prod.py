"""
Ustawienia produkcyjne — nadpisują pakiet tematyczny (base/auth/api).

Wszystkie trzy importy są konieczne: sam `base` zgubiłby AUTH_USER_MODEL
(auth.py) oraz konfigurację DRF/JWT (api.py) i API stanęłoby na AllowAny.
"""
import os

from .base import *
from .auth import *
from .api import *

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Domena podawana przez środowisko (compose), np. mission.twojadomena.pl
_HOST = os.environ.get('DJANGO_ALLOWED_HOST', 'mission.localhost')
ALLOWED_HOSTS = [_HOST]
CSRF_TRUSTED_ORIGINS = [f'https://{_HOST}']

# Front i API pod jedną domeną — CORS nie występuje.
CORS_ALLOWED_ORIGINS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'mission'),
        'USER': os.environ.get('POSTGRES_USER', 'mission'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# HTTPS kończy Caddy i rozmawia z gunicornem po HTTP — bez tego nagłówka
# Django uznałoby połączenie za niezabezpieczone.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Aplikacja nie wysyła maili — konsolowy backend z base.py zostaje celowo.
SILENCED_SYSTEM_CHECKS = ['mail.E001']
