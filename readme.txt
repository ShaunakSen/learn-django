Creating our first app
______________________________


Any main component of our website in Django is called an app

Each App should do one thing!
Else break it up more
We should be able to explain what an app does in 1 sentence

Create a new app:

python manage.py startapp music

A new directory called music gets created
music
    -\migrations
    -__init__.py
    -admin.py
    -apps.py
    -models.py
    -tests.py
    -views.py


\migrations: way that we can connect our website(all of our source code) to our database

__init__: treats the parent directory as a package

admin: Admin section built in

apps: Settings for current app

models: blueprint for our database

views: functions: take a user request and renders something

__________________________________



http://127.0.0.1:8000/admin/: this is the admin section

Whenever we hit a URL django looks in /website/urls.py

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

r: reg exp
^: beginning
$: end

Create file /music/urls.py

from django.conf.urls import url
from . import views

. -> look in same directory












