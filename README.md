# django
Django Initial Project

# Install Python
# Install VirtualEnv `pip install virtualenv`
# Create a virtualenv `virtualenv venv`
# Activate virtualenv `venv\Scripts\activate`
# Install Django `pip install django`
# Install django-environ `pip install django-environ`
# Create Django project `django-admin startproject PROJECT_NAME`
# Change directory to project
# Create Application `python manage.py startapp APP_NAME`
# Migrate the models `python manage.py migrate`
# Create super user `python manage.py createsuperuser`
# First run `python manage.py runserver`
# Run with specified settings file `python manage.py runserver --settings=PROJECT_NAME.SETTINGS_FILE_NAME`

# (django-environ quick start)[https://django-environ.readthedocs.io/en/latest/quickstart.html#usage]

# Separate settings file for different environments [base, development, production]
```
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
```
```
SERVER=production

DEBUG=False

ALLOWED_HOSTS=['*']

# # secret key
SECRET_KEY='secretKey'

# # database
# DB_NAME=
# DB_USER=
# DB_PASSWORD=
# DB_HOST=
# DB_PORT=
```

# [Deployment checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- check --deploy
  `python manage.py check --deploy`
- critical settings
  - SECRET_KEY
  - DEBUG
- environment specific settings
  - ALLOWED_HOSTS
  - CACHES
  - DATABASES
  - EMAIL_BACKEND
  - STATIC_ROOT & STATIC_URL
  - MEDIA_ROOT & MEDIA_URL
- https
  - CSRF_COOKIE_SECURE
  - SESSION_COOKIE_SECURE
- performance optimization
  - sessions
  - CONN_MAX_AGE
  - templates
- error reporting
  - logging
  - admins and managers
  - customize the default error views