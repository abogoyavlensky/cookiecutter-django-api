"""
    core/exceptions.py
    ~~~~~~~~~~~~~~~~~~

    Common exception tools.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
import sys
from collections import OrderedDict

from rest_framework.views import exception_handler as origin_exception_handler


def get_service_name(view):
    """Returns service name by view and stacktrace."""
    service_name = '.'.join(
        [view.__class__.__module__, view.__class__.__name__])
    _, _, tb = sys.exc_info()
    tb = getattr(tb, 'tb_next', tb)
    lineno = getattr(tb, 'tb_lineno', '')
    return ':'.join([service_name, str(lineno)])


def common_exception_handler(exc, context):
    """Add exception format with module and error name details."""
    response = origin_exception_handler(exc, context)
    if response is None:
        return response

    # Detail
    if isinstance(response.data, dict):
        detail = response.data.get('detail')
    else:
        detail = None

    if not detail:
        detail = response.data

    if isinstance(detail, str):
        detail = [detail]
    # Result
    response.data = OrderedDict([
        ('service_name', get_service_name(context.get('view'))),
        ('error_name', exc.__class__.__name__),
        ('detail', detail),
    ])
    return response
