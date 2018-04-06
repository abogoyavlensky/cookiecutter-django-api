"""
    users/models.py
    ~~~~~~~~~~~~~~~

    Models for users app.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Customized user model class."""

    def __str__(self):
        return self.username
