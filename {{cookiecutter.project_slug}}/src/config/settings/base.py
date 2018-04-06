"""
    config/settings/base.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Base settings for {{cookiecutter.project_name}} project.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
import os
from datetime import timedelta

import environ

# PATHS
# -----------------------------------------------------------------------------
# (./config/settings/base.py - 3 = .)
ROOT_DIR = environ.Path(__file__) - 4
# (./config/settings/base.py - 3 = .)
BASE_DIR = environ.Path(__file__) - 3

# ENV
# -----------------------------------------------------------------------------
# Load operating system environment variables and then prepare to use them
env = environ.Env()
# .env file, should load only in development environment
if os.path.exists(ROOT_DIR('.env')):
    env_file = ROOT_DIR('.env')
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')


# GENERAL
# -----------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=False)
# SECRET_KEY must be overriden in production: `$openssl rand -base64 64`
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='0Bm3Y22thf7F6cpSVheG1SZSFdm33RBXhSShGrKs47SBLAQduE')
# ALLOWED_HOSTS must be overriden in production
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS',
                         default=['*'])

SITE_ID = 1
# Timezone and locale
TIME_ZONE = '{{cookiecutter.time_zone}}'
LANGUAGE_CODE = 'en-us'
LANGUAGES = (('en', 'English'), )
USE_I18N = True
USE_L10N = True
USE_TZ = True

# APPLICATIONS
# -----------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
]
THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'django_requestlogging',
]
LOCAL_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.logging_filters.RequestLoggingMiddleware',
]

# DATABASE
# -----------------------------------------------------------------------------
DATABASES = {
    'default': env.db('DATABASE_URL',
                      default='postgres://postgres:@postgres:5432/app'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)

# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR('templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'core.contextprocessors.from_settings',
            ],
        },
    },
]

# STATIC FILES
# -----------------------------------------------------------------------------
STATIC_ROOT = BASE_DIR('staticfiles')
STATIC_URL = '/static/'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE

# MEDIA
# -----------------------------------------------------------------------------
MEDIA_ROOT = BASE_DIR('media')
MEDIA_URL = '/media/'

# URL
# -----------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# -----------------------------------------------------------------------------
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

# AUTHENTICATION
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# Custom user app defaults
AUTH_USER_MODEL = 'users.User'
# Simple JWT
ACCESS_TOKEN_LIFETIME = timedelta(days=7)
REFRESH_TOKEN_LIFETIME = timedelta(days=14)

# CELERY
# -----------------------------------------------------------------------------
INSTALLED_APPS += ['taskapp.celery.CeleryConfig']
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TIMEZONE = TIME_ZONE

# ADMIN
# -----------------------------------------------------------------------------
ADMIN_URL = env('DJANGO_ADMIN_URL', default=r'^admin/')
ADMIN_SITE_HEADER = '{{cookiecutter.project_name}}'
ENVIRONMENT_NAME = env('DJANGO_ENVIRONMENT_NAME', default='DEVELOPMENT')
ENVIRONMENT_COLOR = env('DJANGO_ENVIRONMENT_COLOR', default='gray')

# CACHING
# -----------------------------------------------------------------------------
REDIS_URL = env('REDIS_URL', default='redis://redis')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # keep system run even if redis failed
        }
    }
}

# LOGGING
# -----------------------------------------------------------------------------
LOGGING_APP_LABEL = '{{cookiecutter.project_slug}}'
LOGHANDLER = 'console'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry', LOGHANDLER],
    },
    'filters': {
        'request': {
            '()': 'core.logging_filters.RequestIdFilter',
        },
    },
    'formatters': {
        'default': {
            'format': '%(app_label)s: %(levelname)s [%(request_id)s] '
                      '%(name)s:%(lineno)s %(remote_addr)s %(username)s '
                      '"%(request_method)s %(path_info)s %(server_protocol)s" '
                      '%(http_user_agent)s %(message)s %(asctime)s',
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',  # noqa
            'filters': ['request'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['request'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': [LOGHANDLER],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': [LOGHANDLER],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': [LOGHANDLER],
            'propagate': False,
        },
    },
}

# SENTRY
# -----------------------------------------------------------------------------
DJANGO_SENTRY_DSN = env('DJANGO_SENTRY_DSN', default='')
if DJANGO_SENTRY_DSN:
    import logging  # noqa
    INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]
    RAVEN_CONFIG = {
        'dsn': DJANGO_SENTRY_DSN,
        'environment': env('DJANGO_SENTRY_ENVIRONMENT', default='staging'),
        'tags': {
            'app_label': LOGGING_APP_LABEL,
        }
    }
    RAVEN_MIDDLEWARE = [
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware']  # noqa
    MIDDLEWARE = RAVEN_MIDDLEWARE + MIDDLEWARE

# DEBUG AND PROFILING
# -----------------------------------------------------------------------------
# Enable django-debug-toolbar
USE_DEBUG_TOOLBAR = env.bool('DJANGO_USE_DEBUG_TOOLBAR', default=False)
if DEBUG and USE_DEBUG_TOOLBAR:
    # Tricks to have debug toolbar when developing with docker
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
    INTERNAL_IPS += [ip[:-1] + '1']

    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    INSTALLED_APPS += ['debug_toolbar', ]
    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }
# Enable django-silk
USE_DJANGO_SILK = env.bool('DJANGO_USE_SILK', default=False)
if DEBUG and USE_DJANGO_SILK:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
    INSTALLED_APPS += ['silk']
    SILKY_PYTHON_PROFILER = True
    SILKY_META = True

# REST FRAMEWORK
# -----------------------------------------------------------------------------
PER_PAGE_DEFAULT = 20
SEARCH_PARAM = 'q'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'core.exceptions.common_exception_handler',
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': PER_PAGE_DEFAULT,
    'SEARCH_PARAM': SEARCH_PARAM,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',  # noqa
    'DEFAULT_VERSION': 'v1',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}
DJANGO_SHOW_API_DOCS = env.bool('DJANGO_SHOW_API_DOCS', default=False)

# DJANGO EXTENSIONS
# -----------------------------------------------------------------------------
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
    'exclude_models': ('AbstractBaseSession,Profile,Response,Request,SQLQuery,'
                       'BaseProfile,AbstractBaseUser,AbstractUser,'
                       'PermissionMixin,TimeStampedModel')
}
