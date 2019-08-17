import os

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    import django_heroku
    django_heroku.settings(locals())
