from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    join_date = models.DateTimeField('date published', auto_now_add=True)
    website_name = models.CharField("How you are addressed by the website (can be silly)", max_length=50)
    group_name = models.CharField("How you are addressed by those in your groups", max_length=50)
    def __unicode__(self):
        return self.group_name;
    class Meta:
        ordering = ['join_date']
        
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

