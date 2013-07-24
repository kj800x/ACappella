from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    arranger = models.ForeignKey(User)
    name = models.CharField('group name',max_length=50)
class Song(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField('song title', max_length=50)
    pub_date = models.DateTimeField('date published')
class Track(models.Model):
    song = models.ForeignKey(Song)
    name = models.CharField('track name' ,max_length=50)
    static_location = models.CharField('static location for this audio file', max_length=100)
    
