from core.contextprocessors import from_settings


def test_from_settings(rf, settings):
    settings.ENVIRONMENT_NAME = 'TESTING'
    settings.ENVIRONMENT_COLOR = 'black'
    request = rf.get('users:token-obtain')
    data = from_settings(request)
    assert data['ENVIRONMENT_NAME'] == 'TESTING'
    assert data['ENVIRONMENT_COLOR'] == 'black'
