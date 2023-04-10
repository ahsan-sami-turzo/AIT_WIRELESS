"""
Django settings for Notifier project.

Generated by 'django-admin startproject' using Django 4.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import environ
from pathlib import Path
from datetime import datetime, timedelta

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1', '.ambalawireless.com']

CSRF_TRUSTED_ORIGINS = ['http://*.127.0.0.1', 'https://*.ambalawireless.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'corsheaders',
    'psqlextra',
    'sass_processor',
    'rest_framework',
    'rest_framework.authtoken',
    'django_celery_beat',
    'nf_core',
    'nf_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'Notifier.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Notifier.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'psqlextra.backend',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS')
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

APP_NAME = env('APP_NAME')
APP_CURRENCY = env('APP_CURRENCY')
APP_CURRENCY_SYMBOL = env('APP_CURRENCY_SYMBOL')

LOGIN_URL = 'auth.login'

# CELERY
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER':
        'rest_framework_friendly_errors.handlers.friendly_exception_handler'
    ,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',
}

PSQLEXTRA_PARTITIONING_MANAGER = 'Notifier.partitioning.manager'

PORTAL_URL = env('PORTAL_URL')

MOBIREACH_USERNAME = env('MOBIREACH_USERNAME')
MOBIREACH_PASSWORD = env('MOBIREACH_PASSWORD')

INFOZILLION_USERNAME = env('INFOZILLION_USERNAME')
INFOZILLION_PASSWORD = env('INFOZILLION_PASSWORD')
INFOZILLION_APIKEY = env('INFOZILLION_APIKEY')
INFOZILLION_URL = env('INFOZILLION_BASE_URL')
INFOZILLION_DELIVERYSTATUS_URL = env('INFOZILLION_DELIVERYSTATUS_URL')
INFOZILLION_CLI = env('INFOZILLION_CLI')

GW_PROVIDERS = {
    '013': 'Grameenphone',
    '017': 'Grameenphone',
    '014': 'Banglalink',
    '019': 'Banglalink',
    '015': 'TeleTalk',
    '016': 'Robi',
    '018': 'Robi',

    '035': 'BanglaPhone',
    '036': 'Telebarta',
    '037': 'NationalPhone',
    '038': 'PeoplesTel',
    '044': 'RanksTel',
    '060': 'BijoyPhone',
    '064': 'Onetel',
    '066': 'DhakaPhone',
    '042': 'ShebaPhone',
}
