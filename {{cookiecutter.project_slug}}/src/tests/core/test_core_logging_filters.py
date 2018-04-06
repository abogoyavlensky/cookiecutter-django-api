from core.logging_filters import RequestIdFilter


def test_request_id_filter_attached_additional_attrs(rf, mocker):
    request = rf.get('users:token-obtain')
    obj = RequestIdFilter(request)
    record = mocker.Mock()
    result = obj.filter(record)
    assert result
    assert hasattr(record, 'request_id')
    assert hasattr(record, 'app_label')
