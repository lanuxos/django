"""
Production settings file, extended from base.py
python manage.py runserver --settings=mysite.production
"""

from pathlib import Path
from .base import *
import environ

# django-environ
env = environ.Env(DEBUG=bool, ALLOWED_HOSTS=list)
env_file = BASE_DIR / 'mysite/.env'
environ.Env.read_env(env_file=env_file, overwrite=True)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')



