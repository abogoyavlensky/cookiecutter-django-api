from rest_framework.exceptions import APIException

from core.exceptions import common_exception_handler


def test_common_exception_handler_if_error_without_detail(mocker):
    exp = APIException({'data': 'test'})
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service_name'] == 'unittest.mock.Mock:'
    assert response.data['error_name'] == 'APIException'
    assert response.data['detail'] == {'data': 'test'}


def test_common_exception_handler_if_error_is_string(mocker):
    exp = APIException(['testing error'])
    response = common_exception_handler(exp, mocker.Mock())
    assert response.data['service_name'] == 'unittest.mock.Mock:'
    assert response.data['error_name'] == 'APIException'
    assert response.data['detail'] == ['testing error']
