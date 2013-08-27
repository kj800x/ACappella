from django.conf.urls import patterns, include, url

urlpatterns = patterns('acappellaapp.singerviews',
    url(r'^findgroup$', 'findgroup', name='findgroup'),
    url(r'^(?P<group_short_code>[^/]+)/$', 'displaygroup', name='displaygroup'),
    url(r'^(?P<group_short_code>[^/]+)/(?P<song_short_code>[^/]+)/$', 'displaysong', name='displaysong'),
    url(r'^(?P<group_short_code>[^/]+)/(?P<song_short_code>[^/]+)/makeamixdown/$', 'makeamixdown', name='makeamixdown'),
)
