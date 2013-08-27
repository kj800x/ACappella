from django.conf.urls import patterns, include, url

urlpatterns = patterns('acappellaapp.arrangerviews',
    url(r'^$', 'home', name='arrangerhome'),
    url(r'^profile/$', 'profile', name='arrangerprofile'),
    url(r'^group/(?P<group_short_code>[^/]+)/$', 'grouphome', name='arrangergrouphome'),
    url(r'^group/(?P<group_short_code>[^/]+)/song/(?P<song_short_code>[^/]+)/$', 'songhome', name='arrangersonghome'),
    url(r'^group/(?P<group_short_code>[^/]+)/song/(?P<song_short_code>[^/]+)/upload/track/$', 'uploadtrack', name='arrangeruploadtrack'),
    url(r'^group/(?P<group_short_code>[^/]+)/song/(?P<song_short_code>[^/]+)/upload/pdf/$', 'uploadpdf', name='arrangeruploadpdf'),
)

