"""
    taskapp/celery.py
    ~~~~~~~~~~~~~~~~~

    Main celery app config.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
import os
import sys

from celery import Celery
from django.apps import AppConfig, apps
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Set `apps` dir as PYTHONPATH for celery
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Celery('{{cookiecutter.project_slug}}')


class CeleryConfig(AppConfig):
    """Celery config class."""
    name = 'taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        """Enable django and sentry config for celery."""
        # current_path = os.path.dirname(os.path.abspath(__file__))
        # sys.path.append(os.path.join(current_path, 'apps'))

        app.config_from_object('django.conf:settings')
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration

            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal
            from raven.contrib.celery import register_logger_signal

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['dsn'])
            register_logger_signal(raven_client)
            register_signal(raven_client)


@app.task(bind=True)
def debug_task(self):
    """Simple testing task to debug celery."""
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
