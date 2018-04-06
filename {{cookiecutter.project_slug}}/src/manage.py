"""
    manager.py
    ~~~~~~~~~~

    Main django application module.

    :copyright: (c) 2018 by {{cookiecutter.author}}.
"""
import os
import sys
from django.core.management import execute_from_command_line


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, 'apps'))

    execute_from_command_line(sys.argv)
