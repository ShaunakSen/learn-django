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

url(r'^music/', include('music.urls'))

Now ake a urls.py file in music/

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]


r'^$': index of music app
so route is /music/


In music/views.py

from django.http import HttpResponse

def index(request):
    return HttpResponse('<h1>Music App Home</h1>')

Database Setup
___________________

Django came with default db db.sqlite3

In /website/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

-- these are the default apps django came with

Some of these apps need a db to work

When we run our app

python manage.py runserver

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

-- this means all our source code is not in sync with our db

python manage.py migrate

What happens here is it goes in settings.py to INSTALLED_APPS section
for each app it goes into that app directory and looks for what tables are needed to work with that app

Creating Models
__________________

id is PRIMARY KEY. It is automatically created by Django


from django.db import models

# Create your models here.


class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000)


# Song needs to be associated with an Album
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)




on_delete=models.CASCADE: many songs may be part of an album
But what happens when u delete the album??
here any songs linked to deleted album also get deleted


Now go to /website/settings.py

INSTALLED_APPS = [
    'music.apps.MusicConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

Add 'music.apps.MusicConfig' to INSTALLED_APPS

python manage.py makemigrations music

Migrations for 'music':
  0001_initial.py:
    - Create model Album
    - Create model Song

We made some changes to music model so we run this command

Basically what happens here is it takes all the code in models(classes) and converts them to sql:

E:\my_projects\learn-django\website>python manage.py sqlmigrate music 0001
BEGIN;
--
-- Create model Album
--
CREATE TABLE "music_album" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "artist" varchar(250) NOT NULL, "album_title" varchar(500) NOT NULL, "genre" varchar(100) NOT NULL, "album_
logo" varchar(1000) NOT NULL);
--
-- Create model Song
--
CREATE TABLE "music_song" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "file_type" varchar(10) NOT NULL, "song_title" varchar(250) NOT NULL, "album_id" integer NOT NULL REFERENCES
 "music_album" ("id"));
CREATE INDEX "music_song_95c3b9df" ON "music_song" ("album_id");

COMMIT;

So now we have this sql file

Run it:

python manage.py migrate

Now db is in sync with our code

Whenever we runserver it goes into /website/settings.py

It looks at INSTALLED_APPS
for each INSTALLED_APP it looks at the model
it reviews it and sees if structure of data in code is in sync with db

Django Database API
____________________________

python manage.py shell

It runs Django Database API shell

python manage.py shell
>>> from music.models import Album, Song
>>> Album.objects.all()
[]
>>> a = Album(artist="Taylor Swift", album_title="Red", genre="Country", album_logo="http://www.lyricsmode.com/i/bpictures/10381.png")
>>> a
<Album: Album object>
>>> a.save()
>>> Album.objects.all()
[<Album: Album object>]
>>> a.id
1
>>> b = Album()
>>> b.artist = "Myth"
>>> b.album_title = "High School"
>>> b.genre = "Punk"
>>> b.album_logo = "http://cdn.klimg.com/kapanlagi.com//p/taylor91112a.jpg"
>>> b.save()
>>> a.artist
'Taylor Swift'
>>> b.artist
'Myth'
>>> b.album_title = "Middle School"
>>> b.save()
>>> Album.objects.all()
[<Album: Album object>, <Album: Album object>]

[<Album: Album object>, <Album: Album object>]: is not really useful

In models.py:

# String representation
    def __str__(self):
        return self.album_title + ' - ' + self.artist

Exit shell and restart

>>> from music.models import Album, Song
>>> Album.objects.all()
[<Album: Red - Taylor Swift>, <Album: Middle School - Myth>]

>>> Album.objects.filter(id=1)
[<Album: Red - Taylor Swift>]

>>> Album.objects.filter(artist__startswith="Tay")
[<Album: Red - Taylor Swift>]




















