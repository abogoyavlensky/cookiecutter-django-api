"""
    core/apps.py
    ~~~~~~~~~~~~

    Config for core app.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    """Config for core app."""
    name = 'core'
    verbose_name = _('Core')
