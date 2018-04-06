import pytest
from django.contrib.auth import get_user_model
from django_dynamic_fixture import G


@pytest.mark.django_db
def test_create_user_with_username_ok():
    user = G(get_user_model(), username='test')
    assert user.username == 'test'
    assert str(user) == 'test'
