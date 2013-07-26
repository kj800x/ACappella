from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    arranger = models.ForeignKey(User)
    name = models.CharField('group name',max_length=50)
    short_code = models.CharField('unique, URL ready, shortcode', max_length=50)
    def __unicode__(self):
        return self.name;
    class Meta:
        ordering = ['name']

class Song(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField('song title', max_length=50)
    pub_date = models.DateTimeField('date published')
    short_code = models.CharField('unique, URL ready, shortcode', max_length=50)
    def __unicode__(self):
        return self.title;
    class Meta:
        ordering = ['-pub_date']
        
class Track(models.Model):
    song = models.ForeignKey(Song)
    name = models.CharField('track name' ,max_length=50)
    static_location = models.CharField('static location for this audio file', max_length=100)
    def __unicode__(self):
        return self.name + " (" + self.song.title + ")";
