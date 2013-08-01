from django.contrib import admin
from acappellaapp.models import Group, Song, Track, UserProfile

admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(Song)
admin.site.register(Track)

