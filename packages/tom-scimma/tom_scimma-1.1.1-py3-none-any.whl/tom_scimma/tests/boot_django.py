# boot_django.py
#
# This file sets up and configures Django. It's used by scripts that need to
# execute as if running in a Django server.

import os
import django
from django.conf import settings

APP_NAME = 'tom_scimma'  # the stand-alone app we are testing

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), APP_NAME))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django_extensions',
            'tom_targets',
            'tom_observations',
            'tom_alerts',
            APP_NAME,  # defined above
        ),
        EXTRA_FIELDS={},
        TIME_ZONE='UTC',
        USE_TZ=True,
        BROKERS={
            'SCIMMA': {
                'url': 'http://skip.dev.hop.scimma.org',
                'api_key': '',
                'hopskotch_url': 'dev.hop.scimma.org',
                'hopskotch_username': os.getenv('HOPSKOTCH_USERNAME', ''),
                'hopskotch_password': os.getenv('HOPSKOTCH_PASSWORD', ''),
                'default_hopskotch_topic': ''
            }
        }
    )
    django.setup()
