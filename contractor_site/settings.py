"""Production settings for contractor_site
- يعتمد على env vars (Railway / Render / Heroku style).
- لا تضع هذا الملف مع مفاتيح سرية؛ استخدم env vars في السيرفر.
"""

from pathlib import Path
import os
import logging
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env only if exists (for local testing)
if (BASE_DIR / '.env').exists():
    load_dotenv(BASE_DIR / '.env')

def get_bool_from_env(key, default_value='False'):
    value = os.environ.get(key, default_value)
    return str(value).lower() in ('true', '1', 'yes', 'on')

# -------------------------------------------------------------------------
# Basic / Security
# -------------------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-prod-secret-key')
DEBUG = get_bool_from_env('DEBUG', 'False')

# Allowed Hosts (يرجى تحديد أسماء النطاقات الفعلية)
ALLOWED_HOSTS = []
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS').split(',') if h.strip()]

# CSRF Trusted Origins (يجب أن يكون لكل عنوان البروتوكول https://)
CSRF_TRUSTED_ORIGINS = []
if os.environ.get('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS = [u.strip() for u in os.environ.get('CSRF_TRUSTED_ORIGINS').split(',') if u.strip()]

# -------------------------------------------------------------------------
# Proxy header (for PaaS behind load balancer)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# -------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','compressor',
    'core','services','portfolio','contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contractor_site.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ],},
}]
WSGI_APPLICATION = 'contractor_site.wsgi.application'

# -------------------------------------------------------------------------
# Database
DATABASE_URL = os.environ.get('DATABASE_URL')
DB_LIVE = get_bool_from_env('DB_LIVE', 'False')

if DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=get_bool_from_env('DB_SSL_REQUIRE', 'True'))}
elif DB_LIVE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3','NAME': BASE_DIR / 'db.sqlite3'}}

# -------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# I18N / Timezone
LANGUAGE_CODE = 'ar'
LANGUAGES = [('ar', 'Arabic'), ('en', 'English')]
TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Aden')
USE_I18N = True
USE_TZ = True

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

USE_S3 = get_bool_from_env('USE_S3', 'False')
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', None)
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

COMPRESS_ENABLED = not DEBUG
COMPRESS_ROOT = STATIC_ROOT

# Security
SECURE_SSL_REDIRECT = get_bool_from_env('SECURE_SSL_REDIRECT', str(not DEBUG))
SESSION_COOKIE_SECURE = get_bool_from_env('SESSION_COOKIE_SECURE', str(not DEBUG))
CSRF_COOKIE_SECURE = get_bool_from_env('CSRF_COOKIE_SECURE', str(not DEBUG))

if get_bool_from_env('ENABLE_HSTS', str(not DEBUG)):
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool_from_env('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True')
    SECURE_HSTS_PRELOAD = get_bool_from_env('SECURE_HSTS_PRELOAD', 'True')

X_FRAME_OPTIONS = 'DENY'

# Email (example: uncomment and set env vars to enable)
# EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
# ...

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = {'version': 1,'disable_existing_loggers': False,'handlers': {'console': {'class': 'logging.StreamHandler'}},'root': {'handlers': ['console'], 'level': LOG_LEVEL}}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# """
# Production settings for contractor_site
# - يعتمد على env vars (Railway / Render / Heroku style).
# - لا تضع هذا الملف مع مفاتيح سرية؛ استخدم env vars في السيرفر.
# """

# from pathlib import Path
# import os
# import dj_database_url
# from dotenv import load_dotenv

# load_dotenv()

# def get_bool_from_env(key, default_value='False'):
#     """Helper to convert env string to boolean."""
#     value = os.environ.get(key, default_value)
#     return str(value).lower() in ('true', '1', 'yes', 'on')


# BASE_DIR = Path(__file__).resolve().parent.parent

# # Load local .env only if exists (for local testing)
# if (BASE_DIR / '.env').exists():
#     load_dotenv(BASE_DIR / '.env')

# # -----------------------------------------------------------------------------
# # Basic / Security
# # -----------------------------------------------------------------------------
# SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-prod-secret-key')
# DEBUG = get_bool_from_env('DEBUG', 'False')

# # Allowed Hosts
# ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
# if ALLOWED_HOSTS_ENV:
#     ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]
# else:
#     ALLOWED_HOSTS = ['*']

# # CSRF Trusted Origins
# CSRF_TRUSTED_ORIGINS_ENV = os.environ.get('CSRF_TRUSTED_ORIGINS')
# if CSRF_TRUSTED_ORIGINS_ENV:
#     CSRF_TRUSTED_ORIGINS = [url.strip() for url in CSRF_TRUSTED_ORIGINS_ENV.split(',')]
# else:
#     CSRF_TRUSTED_ORIGINS = ["https://easygoing-love.up.railway.app", "https://www.albazeli.com", "http://127.0.0.1:8000"]

# print(f"DEBUG: {DEBUG}")
# print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")



# # Proxy header (for PaaS behind load balancer)
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # -----------------------------------------------------------------------------
# # Apps / Middleware
# # -----------------------------------------------------------------------------
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     'rest_framework',
#     'compressor',

#     'core',
#     'services',
#     'portfolio',
#     'contact',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',  # serve static
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'contractor_site.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'contractor_site.wsgi.application'

# # Database Configuration
# # Priority:
# # 1. DATABASE_URL (Railway/Production)
# # 2. Local SQLite (Default/Fallback)

# DATABASE_URL = os.environ.get('DATABASE_URL')
# DB_LIVE = get_bool_from_env('DB_LIVE', 'False')

# DATABASES = {}

# if DATABASE_URL:
#     DATABASES['default'] = dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
#     print("Using Database config from DATABASE_URL.")
# elif DB_LIVE:
#     # Fallback to manual postgres vars if DATABASE_URL is missing but DB_LIVE is True
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.environ.get('DB_NAME'),
#             'USER': os.environ.get('DB_USER'),
#             'PASSWORD': os.environ.get('DB_PASSWORD'),
#             'HOST': os.environ.get('DB_HOST'),
#             'PORT': os.environ.get('DB_PORT'),
#         }
#     }
#     print("Using Manual Postgres Config.")
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
#     print("Using Local SQLite3 Database.")

# # Password validation
# # -----------------------------------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

# # -----------------------------------------------------------------------------
# # I18N / Timezone
# # -----------------------------------------------------------------------------
# LANGUAGE_CODE = 'ar'
# LANGUAGES = [('ar', 'Arabic'), ('en', 'English')]
# TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Aden')
# USE_I18N = True
# USE_TZ = True

# # -----------------------------------------------------------------------------
# # Static & Media
# # -----------------------------------------------------------------------------
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'static']

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder',
# ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # Media: by default local; optional S3 if USE_S3=True
# USE_S3 = os.getenv('USE_S3', 'False').lower() in ('true','1','yes')
# if USE_S3:
#     # requires: django-storages[boto3]
#     AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
#     AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
#     AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
#     AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', None)
#     AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#     MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
# else:
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = BASE_DIR / 'media'

# # -----------------------------------------------------------------------------
# # Compressor
# # -----------------------------------------------------------------------------
# COMPRESS_ENABLED = not DEBUG
# COMPRESS_ROOT = STATIC_ROOT

# # -----------------------------------------------------------------------------
# # Security hardening (production-friendly defaults)
# # -----------------------------------------------------------------------------
# # Security hardening
# # Enable SSL Redirect only if not DEBUG, or explicitly forced.
# SECURE_SSL_REDIRECT = get_bool_from_env('SECURE_SSL_REDIRECT', str(not DEBUG))
# SESSION_COOKIE_SECURE = get_bool_from_env('SESSION_COOKIE_SECURE', str(not DEBUG))
# CSRF_COOKIE_SECURE = get_bool_from_env('CSRF_COOKIE_SECURE', str(not DEBUG))

# # HSTS
# if get_bool_from_env('ENABLE_HSTS', str(not DEBUG)):
#     SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = get_bool_from_env('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True')
#     SECURE_HSTS_PRELOAD = get_bool_from_env('SECURE_HSTS_PRELOAD', 'True')


# X_FRAME_OPTIONS = 'DENY'

# # -----------------------------------------------------------------------------
# # Email (example: SendGrid / SMTP)
# # -----------------------------------------------------------------------------
# # EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
# # EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.sendgrid.net')
# # EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
# # EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true','1','yes')
# # EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
# # EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
# # DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@yourdomain.com')

# # -----------------------------------------------------------------------------
# # Logging
# # -----------------------------------------------------------------------------
# LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {'console': {'class': 'logging.StreamHandler'}},
#     'root': {'handlers': ['console'], 'level': LOG_LEVEL},
# }

# # -----------------------------------------------------------------------------
# # Misc
# # -----------------------------------------------------------------------------
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
