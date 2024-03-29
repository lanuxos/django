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

# Django's note
- POST request's data
  ```
  if request.method == 'POST':
      data = request.POST.copy()
      eachData = data.get("Dom's name", None)
  ```
- get_FOO_display() [returning human-readable value of the field choice]
  `Model.get_FOO_display() - FOO is the name of the field`
- ignore .get() DoesNotExisted exception
  `instance.objects.filter(condition).first()`
- model's id reference
- `self.id`
- foreign key properties querySet filtering
  ```
  # django querySet filtering via foreign key properties (foreign key value)
  class Author(models.Model):
    name = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
  class Book(models.Model):
    book = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

  book = Book.objects.filter(author__name='FOO') # filter book via author's name
  ```
- UniqueConstraint
  ```
  # as below code, the model will prevent duplication of the field 
  # to ensures each room can only be booked once for each date
  class Meta:
      constraints = [
          models.UniqueConstraint(
              fields = ['room', 'date'], 
              name='unique_booking'
          )
      ]
  ```
- comparing two fields with F() expression
  `var = Model.objects.filter(field1=F('field2'))`
- fixture [dump/load]
  ```
  # dump\load data from fixtures [database initialize]
  # to dump data from database model to fixtures/ directory use below command
  python manage.py dumpdata appName.modelName > fixtures/modelName.json
  python manage.py dumpdata > databasedump.json                # full database
  python manage.py dumpdata myapp > databasedump.json          # only 1 app
  python manage.py dumpdata myapp.mymodel > databasedump.json  # only 1 model (table)
  # to load data from fixtures use following command
  python manage.py loaddata fixtures/modelName
  # json form
  [
    {
      "model": "myapp.person",
      "pk": 1,
      "fields": {
        "first_name": "John",
        "last_name": "Lennon"
      }
    },
    {
      "model": "myapp.person",
      "pk": 2,
      "fields": {
        "first_name": "Paul",
        "last_name": "McCartney"
      }
    }
  ]
  ```
- registering admin models at once
  ```
  from django.apps import apps
  app = apps.get_app_config('APP_NAME')
  for model_name, model in app.models.items():
      admin.site.register(model)
  ```
- redirect to last requested page after login
  ```
  # to get full urls with param/values
  <a href="{% url django.contrib.auth.views.login %}?next={{request.get_full_path|urlencode }}"/>
  # or getting path without parameters
  <a href="{% url django.contrib.auth.views.login %}?next={{request.path }}"/>
  ```
- misc

# Python's note
- max func
  ```
  # python max function, max(ITERABLE, key=int, default='No value to compare')
  list = ['09', '03', '01', '5', '07']
  emptyList = []
  max(list) # return '5'
  max(list, key=int) # return '09'
  max(emptyList, default='No value to compare') # return 'No value to compare'
  ```
- dictionary iteration with index
  ```
  dict = {
      'key1': 'value1',
      'key2': 'value2',
      'key3': 'value3',
  }
  for index, (key, value) in enumerate(dict.items()):
      print(index, key, value)
  ```
- 

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