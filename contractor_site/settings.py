"""
Django settings for contractor_site project.
Production-ready configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ------------------------------------------------------------------------------
# Base
# ------------------------------------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent
# load_dotenv(BASE_DIR / '.env')  # يستخدم محليًا فقط – على السيرفر استعمل env vars
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')  # مفيد محلياً

# ------------------------------------------------------------------------------
# Security
# ------------------------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-prod')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# ALLOWED_HOSTS = your-app.onrender.com
# CSRF_TRUSTED_ORIGINS = https://your-app.onrender.com



# SECRET_KEY = os.getenv(
#     'SECRET_KEY',
#     'insecure-dev-key-change-me'
# )

# DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

# ALLOWED_HOSTS = os.getenv(
#     'ALLOWED_HOSTS',
#     'localhost,127.0.0.1'
# ).split(',')

# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'compressor',

    'core',
    'services',
    'portfolio',
    'contact',
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

# ------------------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------------------
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

WSGI_APPLICATION = 'contractor_site.wsgi.application'

# # ------------------------------------------------------------------------------
# # Database (PostgreSQL)
# # ------------------------------------------------------------------------------
# DATABASE_URL = os.getenv('DATABASE_URL')

# if DATABASE_URL:
#     DATABASES = {
#         'default': dj_database_url.parse(
#             DATABASE_URL,
#             conn_max_age=600
#         )
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('DB_NAME', 'contractor_db'),
#             'USER': os.getenv('DB_USER', 'contractor_user'),
#             'PASSWORD': os.getenv('DB_PASSWORD', ''),
#             'HOST': os.getenv('DB_HOST', 'localhost'),
#             'PORT': os.getenv('DB_PORT', '5432'),
#         }
#     }

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Load environment variables from .env file (for local development)
# Database (use DATABASE_URL provided by Render)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# ------------------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'ar'

LANGUAGES = [
    ('ar', 'Arabic'),
    ('en', 'English'),
]

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Aden')

USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------------------
# Compressor
# ------------------------------------------------------------------------------
COMPRESS_ENABLED = not DEBUG
COMPRESS_ROOT = STATIC_ROOT

# ------------------------------------------------------------------------------
# Security (Production)
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1', 'yes')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    ''
).split(',') if os.getenv('CSRF_TRUSTED_ORIGINS') else []

X_FRAME_OPTIONS = 'DENY'

# ------------------------------------------------------------------------------
# Default primary key field type
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# """
# Django settings for contractor_site project.

# Generated by 'django-admin startproject' using Django 6.0.

# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/6.0/ref/settings/
# """

# import os
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-2l%_&&$2hgdt-0fuvif1td(t7-^s(-b=^u_7de^$3-p4-v&$+4'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# # Application definition

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
#     'whitenoise.middleware.WhiteNoiseMiddleware',
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


# # Database
# # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# # Load environment variables from .env file (for local development)
# env_path = BASE_DIR / '.env'
# if env_path.exists():
#     with open(env_path, encoding='utf-8') as f:
#         for line in f:
#             line = line.strip()
#             if line and not line.startswith('#') and '=' in line:
#                 key, value = line.split('=', 1)
#                 # Strip whitespace from key and value
#                 os.environ.setdefault(key.strip(), value.strip())

# # PostgreSQL Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'contractor_db'),
#         'USER': os.environ.get('DB_USER', 'contractor_user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', '9253'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# # Fallback to SQLite for development if needed
# if os.environ.get('USE_SQLITE', 'False').strip().lower() == 'true':
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }


# # Password validation
# # https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/6.0/topics/i18n/

# LANGUAGE_CODE = 'ar'

# LANGUAGES = [
#     ('ar', 'Arabic'),
#     ('en', 'English'),
# ]

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/6.0/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'static']

# MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'compressor.finders.CompressorFinder',
# )

# COMPRESS_ROOT = STATIC_ROOT
# COMPRESS_ENABLED = True

# # Default primary key field type
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
