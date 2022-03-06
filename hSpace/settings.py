"""
This settings file should be run with docker-compose or just normal python manage.py runserver command
Any change could be make things not working properly, so be careful with that
"""
import os
import platform
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

# from .extra_settings import (CKEDITOR_CONFIGS, SWAGGER_SETTINGS, REDOC_SETTINGS, ELASTICSEARCH_DSL)

# Load our secret keys to use in development .env is being ignored in commit
load_dotenv(dotenv_path=Path('.env'))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Try to load enviroment in docker first if not detected switch to .env file
# SECRET_KEY
DOCKER_DJANGO_SECRET_KEY = os.environ.get('SECRET_KEY')
if DOCKER_DJANGO_SECRET_KEY is not None:
    SECRET_KEY = DOCKER_DJANGO_SECRET_KEY
else:
    SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG
DOCKER_DJANGO_DEBUG = os.environ.get('DEBUG')
if DOCKER_DJANGO_DEBUG is None:
    DEBUG = int(os.getenv('DEBUG')) if os.getenv('DEBUG') else 1
else:
    DEBUG = int(DOCKER_DJANGO_DEBUG)

# ALLOWED_HOSTS
DOCKER_DJANGO_ALLOWED_HOST = os.environ.get('DJANGO_ALLOWED_HOSTS')
if DOCKER_DJANGO_ALLOWED_HOST is not None:
    ALLOWED_HOSTS = DOCKER_DJANGO_ALLOWED_HOST.split(' ')
else:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ') if os.getenv('ALLOWED_HOSTS') \
        else '127.0.0.1 localhost [::1] 13.229.29.156'.split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',  # full text search feature of postgres
    'django.contrib.humanize',
    'easy_select2',
    'drf_yasg',

    'cloudinary',  # CDN upload to cloudinary

    'rest_framework',  # first added if you want to use djangorestframework
    'rest_framework.authtoken',  # See REST_FRAMEWORK settings below
    'corsheaders',  # Avoid CORS policy
    # User created app
    'event.apps.EventConfig',
    'ckeditor',  # https://github.com/django-ckeditor/django-ckeditor#installation
    # 'django_elasticsearch_dsl',  # https://elasticsearch-dsl.readthedocs.io/
    # 'django_elasticsearch_dsl_drf',
]

if os.environ.get('USE_S3', os.getenv('USE_S3')) == 'TRUE':
    INSTALLED_APPS += [
        'storages'
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',  # static file serve in production

    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hSpace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hSpace.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# DATABASES
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', os.getenv('DB_ENGINE')),
        'NAME': os.environ.get('DB_NAME', os.getenv('DB_NAME')),
        'USER': os.environ.get('DB_USER', os.getenv('DB_USER')),
        'PASSWORD': os.environ.get('DB_PASSWORD', os.getenv('DB_PASSWORD')),
        'HOST': os.environ.get('DB_HOST', os.getenv('DB_HOST')),
        'PORT': os.environ.get('DB_PORT', os.getenv('DB_PORT'))
    }
}

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', _('English')),
    ('vi', _('Vietnam')),
)

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_USE_SESSIONS = True

# AUTH_USER_MODEL = 'event.User'
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]

# Sending emails settings with sendgrid services
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True if os.getenv('EMAIL_USE_TLS') == 'True' else False
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') if os.getenv('SENDGRID_API_KEY') else None
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = int(os.getenv('EMAIL_PORT')) if os.getenv('EMAIL_PORT') else None
EMAIL_USE_SSL = True if os.getenv('EMAIL_USE_SSL') == 'True' else False
# DEFAULT_FROM_EMAIL = 'hspacesnetwork@gmail.com'  # Default sender email
DEFAULT_FROM_EMAIL = 'support@hspace.biz'  # Default sender email

# Media file cloud storage
CLOUDINARY = {
    'cloud_name': os.getenv('cloud_name'),
    'api_key': os.getenv('api_key'),
    'api_secret': os.getenv('api_secret'),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (  # Setting up Authentication for limiting access to guest user
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'  # Just render raw json response
    ],
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    # For generate documenttation
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CORS_ORIGIN_ALLOW_ALL = True

# Config logging to console during development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
else:
    from datetime import datetime, timedelta

    log_file_name = datetime.today().strftime('%Y-%d-%m')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, f'logs/{log_file_name}.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

# Config local path for translation file
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Cache configuration based on OS
if platform.system() == 'Windows':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
elif platform.system() == 'Linux':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/tmp/memcached.sock',
        }
    }

# Config S3
if os.environ.get('USE_S3', os.getenv('USE_S3')) == 'TRUE':
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', os.getenv('AWS_ACCESS_KEY_ID'))
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', os.getenv('AWS_SECRET_ACCESS_KEY'))
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', os.getenv('AWS_STORAGE_BUCKET_NAME'))
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_DEFAULT_ACL = os.environ.get('AWS_DEFAULT_ACL', os.getenv('AWS_DEFAULT_ACL'))  # 'public-read'

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
    DEFAULT_FILE_STORAGE = 'hSpace.extra_settings.storage_backends.PublicMediaStorage'

    AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
    PRIVATE_FILE_STORAGE = 'hSpace.extra_settings.storage_backends.PrivateMediaStorage'
