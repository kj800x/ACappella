# Create your views here.
from django.shortcuts import render
from acappellaapp.models import Group, Song, Track
from django.http import HttpResponse

def findgroup(request):
    group_list = Group.objects.all()
    context = {'group_list': group_list}
    return render(request, 'findgroup.html', context)

def displaygroup(request, group_short_code):
    group = Group.objects.filter(short_code = group_short_code)[0]
    song_list = Song.objects.filter(group = group);
    context = {'group': group, 'song_list': song_list}
    return render(request, 'displaygroup.html', context)
    
    
def displaysong(request, group_short_code, song_short_code):
    group = Group.objects.filter(short_code = group_short_code)[0]
    song = Song.objects.filter(short_code = song_short_code, group = group)[0]
    track_list = Track.objects.filter(song = song);
    context = {'group': group, 'song': song, 'track_list': track_list}
    return render(request, 'displaysong.html', context)
