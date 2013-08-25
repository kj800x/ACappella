from django.db import models
from django.contrib.auth.models import User
import re;
# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    join_date = models.DateTimeField('Join date', auto_now_add=True)
    website_name = models.CharField("How you are addressed by the website. Ex: Dave Grossman", max_length=50)
    group_name = models.CharField("How you are addressed by those in your groups. Ex: Mr. Grossman", max_length=50)
    def __unicode__(self):
        return self.group_name;
    class Meta:
        ordering = ['join_date']
        
class Group(models.Model):
    arranger = models.ForeignKey(UserProfile)
    name = models.CharField('group name',max_length=50)
    public = models.BooleanField('should the group be listed in the directory?', default=True)
    searchterms = models.TextField('any additional search terms that someone might use to find this group', blank=True)
    latlon = models.TextField('lat:lon for group', blank=True) #in case we do a type of map - search for groups later
    message = models.TextField('message to the group', blank=True)
    short_code = models.SlugField('unique, URL ready, shortcode', max_length=50, unique=True)
    def __unicode__(self):
        return self.name;
    def findshortcode(self, name):
        notalpha = re.compile('[\W]+')
        base = notalpha.sub('', name)
        modifier = 0;
        if not base:
          base = "No_Name_Provided"
        while True:
          if modifier:
            totry = base + str(modifier);
          else:
            totry = base;
          if (not self._default_manager.filter(short_code=totry)):
            return totry;
          modifier = modifier + 1;
    class Meta:
        ordering = ['name']

class Song(models.Model):
    group = models.ForeignKey(Group)
    title = models.CharField('song title', max_length=50)
    pdf_location = models.CharField('static location for this song\'s PDF', max_length=100, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    message = models.TextField('preformance notes', blank=True)
    short_code = models.SlugField('unique, URL ready, shortcode', max_length=50)
    def __unicode__(self):
        return self.title + " (" + self.group.name + ")";
    def findshortcode(self, group, name):
        notalpha = re.compile('[\W]+')
        base = notalpha.sub('', name)
        modifier = 0;
        if not base:
          base = "No_Name_Provided"
        while True:
          if modifier:
            totry = base + str(modifier);
          else:
            totry = base;
          if (not self._default_manager.filter(group=group, short_code=totry)):
            return totry;
          modifier = modifier + 1;
    class Meta:
        ordering = ['-pub_date']
        unique_together = ('short_code', 'group',)
        
class Track(models.Model):
    song = models.ForeignKey(Song)
    name = models.CharField('track name' ,max_length=50)
    location = models.CharField('static location for this audio file', max_length=100)
    def __unicode__(self):
        return self.name + " (" + self.song.title + ")";
        
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

