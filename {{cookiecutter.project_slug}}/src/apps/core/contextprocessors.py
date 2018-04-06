"""
    core/contextprocessors.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Common context processors.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.conf import settings


# pylint: disable=unused-argument
def from_settings(request):
    """Return common settings to admin templates."""
    return {
        'ENVIRONMENT_NAME': settings.ENVIRONMENT_NAME,
        'ENVIRONMENT_COLOR': settings.ENVIRONMENT_COLOR,
    }
