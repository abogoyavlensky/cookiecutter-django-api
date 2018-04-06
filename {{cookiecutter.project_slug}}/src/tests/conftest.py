"""
    tests/conftest.py
    ~~~~~~~~~~~~~~~~~

    Common configuration for tests.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
import os
import sys

import pytest
from django.contrib.auth import get_user_model
from django_dynamic_fixture import G
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user():
    user = G(get_user_model(), username='user')
    user.set_password('user')
    user.save()
    return user


@pytest.fixture
def client(user):
    token = RefreshToken.for_user(user).access_token
    headers = {'HTTP_AUTHORIZATION': 'Bearer {token}'.format(token=token)}
    return APIClient(**headers)


@pytest.fixture
def anon():
    return APIClient()
