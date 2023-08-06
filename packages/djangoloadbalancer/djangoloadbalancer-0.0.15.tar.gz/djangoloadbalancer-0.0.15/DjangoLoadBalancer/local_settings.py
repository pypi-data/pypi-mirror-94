import os

import django
for dirpath, dirnames, files in os.walk('./'):
    if dirpath[len('./'):].count(os.sep) < 1:
        print(files)
        print(f'Found directory: {dirpath}')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LoadBalancer.settings")
django.setup()

from django.conf import settings

LOAD_BALANCER = settings.LOAD_BALANCER
DATABASES = settings.DATABASES
