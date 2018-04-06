"""
    users/apps.py
    ~~~~~~~~~~~~~

    Config for users app.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    """Config for users app."""
    name = 'users'
    verbose_name = _('Users')
