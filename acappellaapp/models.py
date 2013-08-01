from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField("Full Name", max_length=50)

class Group(models.Model):
    arranger = models.ForeignKey(UserProfile)
    name = models.CharField('group name',max_length=50)
    message = models.TextField('message to the group', blank=True)
    short_code = models.CharField('unique, URL ready, shortcode', max_length=50)
    def __unicode__(self):
        return self.name;
    class Meta:
        ordering = ['name']

class Song(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField('song title', max_length=50)
    pub_date = models.DateTimeField('date published')
    message = models.TextField('message to the group about this song', blank=True)
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
        
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

