from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^profile/$', 'acappellaapp.views.arrangerprofile', name='arrangerprofile'),
    url(r'^$', 'acappellaapp.views.arrangerhome', name='arrangerhome'),
    url(r'^group/(?P<group_short_code>[^/]+)/$', 'acappellaapp.views.arrangergrouphome', name='arrangergrouphome'),
    url(r'^group/(?P<group_short_code>[^/]+)/song/(?P<song_short_code>[^/]+)/$', 'acappellaapp.views.arrangersonghome', name='arrangersonghome'),
    url(r'^group/(?P<group_short_code>[^/]+)/song/(?P<song_short_code>[^/]+)/upload/track/$', 'acappellaapp.views.arrangeruploadtrack', name='arrangeruploadtrack'),
)
