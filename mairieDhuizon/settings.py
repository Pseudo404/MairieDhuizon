from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

_env_file = os.environ.get('DJANGO_ENV_FILE', '.env')
load_dotenv(BASE_DIR / _env_file)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'django-insecure-dev-only-ne-pas-utiliser-en-prod'
    else:
        raise ImproperlyConfigured(
            'DJANGO_SECRET_KEY doit être définie en production.'
        )

if DEBUG:
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0,26.221.140.19,26.247.5.195').split(',')
else:
    ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'www.dhuizon.fr,dhuizon.fr').split(',')

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if o.strip()]

if not DEBUG and not CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = ['https://www.dhuizon.fr', 'https://dhuizon.fr']

TRUST_X_FORWARDED_FOR = os.environ.get('TRUST_X_FORWARDED_FOR', 'False') == 'True'
ADMIN_IP_RESTRICTION_ENABLED = os.environ.get('ADMIN_IP_RESTRICTION_ENABLED', 'True') == 'True'
ADMIN_FALLBACK_IPS = os.environ.get('ADMIN_FALLBACK_IPS', '')
ADMIN_ALLOW_LOCALHOST_IN_DEBUG = os.environ.get('ADMIN_ALLOW_LOCALHOST_IN_DEBUG', 'True') == 'True'

if not DEBUG:

    # Force HTTPS → empêche le MITM
    SECURE_SSL_REDIRECT = True

    # Cookies de session uniquement en HTTPS
    SESSION_COOKIE_SECURE = True

    # Cookie CSRF uniquement en HTTPS
    # empêche l’interception du token CSRF (attaque CSRF + MITM)
    CSRF_COOKIE_SECURE = True

    # HTTP Strict Transport Security (HSTS)
    # empêche les downgrade attacks
    SECURE_HSTS_SECONDS = 15768000  # 6 mois

    # protège toute l’architecture contre downgrade HTTPS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # empêche toute connexion HTTP initiale (anti downgrade global)
    SECURE_HSTS_PRELOAD = True

    # évite les fausses détections HTTP derrière reverse proxy
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # protège contre clickjacking (iframe)
    X_FRAME_OPTIONS = 'DENY'

    # protège contre exécution de fichiers mal interprétés (XSS indirect)
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # évite fuite d’URL sensibles vers sites externes
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

    # protège contre vol de token CSRF via XSS
    CSRF_COOKIE_HTTPONLY = True

    # protège contre vol de session via XSS
    SESSION_COOKIE_HTTPONLY = True

    # protège contre CSRF (cross-site request forgery)
    SESSION_COOKIE_SAMESITE = 'Lax'

    # réduit l’impact du vol de session (session hijacking)
    SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 heures

# upload (10 Mo) max
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'mairie-dhuizon',
    }
}

RATELIMIT_VIEW = 'core.views.ratelimited_error'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'core',
]

TAILWIND_APP_NAME = 'theme'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
    'core.middleware.AdminIPRestrictionMiddleware',
    'core.middleware.PageViewTrackingMiddleware',
]

ROOT_URLCONF = 'mairieDhuizon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mairieDhuizon.wsgi.application'

#postgresql
# if os.environ.get('DB_ENGINE') == 'postgresql':
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ.get('DB_NAME', 'mairie_dhuizon'),
#             'USER': os.environ.get('DB_USER', ''),
#             'PASSWORD': os.environ.get('DB_PASSWORD', ''),
#             'HOST': os.environ.get('DB_HOST', 'localhost'),
#             'PORT': os.environ.get('DB_PORT', '5432'),
#         }
#     }
# else:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/assets/'
STATICFILES_DIRS = [BASE_DIR / 'assets']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
BREVO_SENDER_EMAIL = os.environ.get('BREVO_SENDER_EMAIL', 'ne-pas-repondre@dhuizon.fr')
BREVO_SENDER_NAME = os.environ.get('BREVO_SENDER_NAME', 'Mairie de Dhuizon')
BREVO_RECIPIENT_EMAIL = os.environ.get('BREVO_RECIPIENT_EMAIL', 'mairie@dhuizon.fr')
