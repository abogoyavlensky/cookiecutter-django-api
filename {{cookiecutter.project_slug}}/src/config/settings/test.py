"""
Test settings for {{cookiecutter.project_name}} project.

- Used to run tests fast on the continuous integration server and locally
"""

from .base import *  # noqa


# DEBUG
# -----------------------------------------------------------------------------
# Turn debug off so tests run faster
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# TESTING
# -----------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# PASSWORD HASHING
# -----------------------------------------------------------------------------
# Use fast password hasher so tests run faster
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# TEMPLATE LOADERS
# -----------------------------------------------------------------------------
# Keep templates in memory so tests run faster
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ['django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ], ],
]

# CACHING
# -----------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# CELERY
# -----------------------------------------------------------------------------
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# REMOVE SILK
# -----------------------------------------------------------------------------
if 'silk' in INSTALLED_APPS:
    INSTALLED_APPS.remove('silk')
if 'silk.middleware.SilkyMiddleware' in MIDDLEWARE:
    MIDDLEWARE.remove('silk.middleware.SilkyMiddleware')
SILKY_PYTHON_PROFILER = False
