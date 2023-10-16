"""
Development settings file, extended from base.py
python manage.py runserver
"""

from pathlib import Path
from .base import *

SECRET_KEY = 'django-insecure-9n!)kh7n7a)6c0(q15n!)qd2xh&n9!t*au-@khy&)ewk(dnx2i'

DEBUG = True

ALLOWED_HOSTS = []

print("\nYou are using development settings file\n")