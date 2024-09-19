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

# Django Function Based View notes
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
- ImageField/photo management
  - settings.py
  ```
  # set media/static url, staticfiles directory and media root
  STATIC_URL = 'static/'
  STATICFILES_DIRS = [ BASE_DIR / 'static' ]

  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'
  ```
  - urls.py
  ```
  # on application's urls.py add
  # for image/media file display through url
  from . import settings
  from django.contrib.staticfiles.urls import static
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns

  urlpatterns += staticfiles_urlpatterns()
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  ```
  - models.py
  ```
  class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, help_text="ຊື່ຜູ້ໃຊ້")

    def pathAndName(instance, filename):
        upload_to = 'images/userProfile'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    photo = models.ImageField(upload_to=pathAndName, blank=True, null=True, default="media/default.png", help_text="ຮູບພາບ", verbose_name="ຮູບພາບ")
  ```
  - template.html
  ```
  {% if object_list is not None %}
  <img src="{{ object_list.photo.url }}" alt="photoUrl" width="30" height="40">
  {% else %}
  <img src="{% static '../media/default.png' %}" alt="photoUrl" width="30" height="40">
  {% endif %}
  ```

- request IP
```
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # x_forwared_for return a list of ip(s)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
```

- misc

# Django Class Based View notes
- CRUD
    - models.py
```
from django.contrib.auth.models import User
from django.db import models


class SomeModel(models.Model):
    someField = models.CharField(max_length=255)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
```
  - views.py
```
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create
# create MODELNAME_form.html in template folder
class SomeCreateView(CreateView):
    model = MODEL_NAME
    fields = [
        "modelField1",
        "modelField2",
        "modelField3",
    ]
    success_url = "somewhereURLName"


# Create with custom template, no need to create
# MODELNAME_form.html in template directory
class SomeCreateViewWithCustomTemplate(CreateView):
    model = MODEL_NAME
    fields = [
        "modelField1",
        "modelField2",
        "modelField3",
    ]
    success_url = "somewhereURLName"

# Create with request.user
class SomeCreateView(LoginRequiredMixin, CreateView):
    model = SomeModel
    fields = ["someField"]

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

# Read
# ListView return "object_list" context
# create MODELNAME_list.html in template folder
class SomeListView(ListView):
    model = MODEL_NAME


# DetailView return "object" context
# urlpattern MUST specific <pk>
class SomeDetailView(DetailView):
    model = MODEL_NAME


# Update
# create MODELNAME_form.html in template directory
class SomeUpdateView(UpdateView):
    model = MODEL_NAME
    success_url = "SOME_URL_NAME"


# update view with permission/login
class SomeUpdateView(LoginRequiredMixin, UpdateView):
    model = MODEL_NAME
    success_url = "SOME_URL_NAME"


# Delete
# create MODELNAME_confirm_delete.html in template directory
class SomeDeleteView(LoginRequiredMixin, DeleteView):
    model = MODEL_NAME
    success_url = "SOME_URL_NAME"
```
  - template.html
    - MODEL_list.html
```
{% extends 'base.html' %}

{% block content %}
    {% for object in object_list %}
        {{ object.FIELD }}
    {% endfor %}
{% endblock content %}
```

    - MODEL_detail.html
```
{% extends 'base.html' %}

{% block content %}
    {{ object.FIELD }}
{% endblock content %}
```

    - MODEL_form.html
```
{% extends 'base.html' %}

{% block content %}
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" value="Save" class="btn btn-sm btn-success">
    </form>
{% endblock content %}
```

    - MODEL_confirm_delete.html
```
{% extends 'base.html' %}

{% block content %}
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <p>Are you sure, you want to delete "{{ object.title }}"</p>
        <input type="submit" value="Confirm" class="btn btn-sm btn-danger">
    </form>
{% endblock content %}
```

  - urls.py
```
urlpatterns = [
    path("listview/", SomeListView.as_view(), name="listViewPage"),
    path("detail/<pk>", SomeDetailView.as_view(), name="DetailViewPage"),
    path("create/", SomeCreateView.as_view(), name="CreateViewPage"),
    path("update/<pk>", SomeUpdateView.as_view(), name="updateViewPage"),
    path("delete/<pk>", SomeDeleteView.as_view(), name="deleteViewPage"),
]
```

- get_context_data() # for additional context data
  - views.py
```
class SomeCreateView(CreateView):  
    model = MODEL_NAME
    fields = [
        "modelField1",
        "modelField2",
        "modelField3",
    ]
    success_url = "somewhereURLName"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['KEY'] = ADDITIONAL_DATA
        return context
```

- get_queryset() # for specific context data
  - views.py
```
class SomeListView(ListView):  
    model = MODEL_NAME

    def get_queryset(self, **kwargs: Any):
        return MODEL_NAME.objects.filter(FILTER_FIELD=FILTER_KEY)
        # return MODEL.objects.filter(username=self.kwargs["username"])
        # username come along with parameter request
```

- paginarion
  - views.py
```
from django.core.paginator import Paginator # Paginator
# create MODELNAME_list.html in template folder
class SomeListView(ListView):  
    paginate_by = 10    # pagination
    model = MODEL_NAME
```

- crispy_form
  - settings.py
```
INSTALLED_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
]

# crispy_forms_settings
CRISPY_ALLOWD_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

  - template1.html [crispy filter]
```
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form | crispy }}
        <input type="submit" value="Save" class="btn btn-sm btn-success">
    </form>
{% endblock content %}
```

  - template2.html [as_crispy_field filter]
```
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <div class="row">
            <div class="col-sm-12 col-md-3">
                {{ form.FIELD1|as_crispy_field }}
            </div>
            <div class="col-sm-12 col-md-3">
                {{ form.FIELD2|as_crispy_field }}
            </div>
            <div class="col-sm-12 col-md-3">
                {{ form.FIELD3|as_crispy_field }}
            </div>
            <div class="col-sm-12 col-md-3 d-flex align-items-center">
                <input type="submit" value="Save" class="form-control btn btn-sm btn-success">
            </div>
        </div>
    </form>
{% endblock content %}
```

- Mixins
  - SingleObjectMixin
    - views.py
```
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from books.models import Author


class RecordInterestView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""

    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        # Look up the author we're interested in.
        self.object = self.get_object()
        # Actually record interest somehow here!

        return HttpResponseRedirect(
            reverse("author-detail", kwargs={"pk": self.object.pk})
        )
```
    - urls.py
```
from django.urls import path
from books.views import RecordInterestView

urlpatterns = [
    # ...
    path(
        "author/<int:pk>/interest/",
        RecordInterestView.as_view(),
        name="author-interest",
    ),
]
```
  - SingleObjectMixin with ListView


# Django Rest Framework Function Based View notes
- Install Django Rest Framework `pip install djangorestframework`
- serializers.py
```
from rest_framework import serializers
from .models import *

class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName
        fields = ('__all__')
```
- views.py
```
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import *

@api_view(['GET'])
def AllRecords(request):
    allRecords = SomeModel.objects.all()
    serializer = SomeModelSerializer(allRecords, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def Records(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'PATCH':
        pass
    else:
        pass


@api_view(['POST'])
def SaveRecords(request):
    if request.method == 'POST':
        serializer = SomeModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
```
- urls.py
```
from django.urls import path
from .views import *

urlpatterns = [
  path('api/all', AllRecords),
  path('api/new', SaveRecords),
]
```

# Django Rest Framework Class Based View notes
- CRUD
  - views.py
```
# Create
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from myapp.models import Author


class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.accepts("text/html"):
            return response
        else:
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)


class AuthorCreateView(JsonableResponseMixin, CreateView):
    model = SomeModel
    fields = ["someField"]
```

- Django Rest Framework Simple JWT Authorization
  - views.py
```
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class MatabaseAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'test matabase api with jwt'}
        return Response(content)
```
  - urls.py
```
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='tokenObtainPair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/test/', MatabaseAPI.as_view(), name='api_test'),
]
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


# JavaScript's note
- toggle dark mode switch
```html
<div class="form-check form-switch">
  <input class="form-check-input mx-1" type="checkbox" role="switch" id="dark-mode-switch" checked>
  <label class="form-check-label mx-1" for="dark-mode-switch">Light/Dark</label>
</div>
```
``` javascript
document.getElementById("dark-mode-switch").addEventListener("change", () => {
            if (document.getElementById("dark-mode-switch").checked == true) {
                document.documentElement.setAttribute("data-bs-theme", "dark");
            } else {
                document.documentElement.setAttribute("data-bs-theme", "light");
            }
        });
```