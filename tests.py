import os
import sys
import unittest
import doctest
import django
import logging

APP_MODULE = 'jogging'

def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        APP_MODULE,
    )
    global_settings.DATABASE_ENGINE = "sqlite3"
    global_settings.DATABASE_NAME = ":memory:"
    global_settings.ROOT_URLCONF = 'jogging.tests.urls'

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'jogging.middleware.LoggingMiddleware',
    )

    # jogging settings must be set up here.
    from jogging.handlers import DatabaseHandler, MockHandler
    global_settings.GLOBAL_LOG_HANDLERS = []
    global_settings.GLOBAL_LOG_LEVEL = logging.INFO
    global_settings.LOGGING = {}

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1,2):
        test_runner = test_runner()
        failures = test_runner.run_tests([APP_MODULE])
    else:
        failures = test_runner([APP_MODULE], verbosity=1)
    sys.exit(failures)

if __name__ == '__main__':
    main()
