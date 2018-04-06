"""
    core/logging_filters.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Common logging tools.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
from django.conf import settings
from django_requestlogging.logging_filters import RequestFilter
from django_requestlogging.middleware import LogSetupMiddleware


class RequestIdFilter(RequestFilter):
    """Logging filter that adds request id to log message."""

    def filter(self, record):  # flake8: noqa=A002
        """Adds session from the request to the logging `record`."""
        user = getattr(self.request, 'user', None)
        record.request_id = getattr(user, 'id', '-')
        record.app_label = settings.LOGGING_APP_LABEL
        return super(RequestIdFilter, self).filter(record)


class RequestLoggingMiddleware(LogSetupMiddleware):
    """Add RequestIdFilter to every request."""

    def process_request(self, request):
        """Adds a filter, bound to `request`, to the appropriate loggers."""
        request.logging_filter = RequestIdFilter(request)
        self.add_filter(request.logging_filter)
