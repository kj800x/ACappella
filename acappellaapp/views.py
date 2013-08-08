# Create your views here.
from django.shortcuts import render
from acappellaapp.models import Group, Song, Track, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

def check_profile(f):
  def wrapper(*args, **kw):
    if not (args[0].user.profile.website_name and args[0].user.profile.group_name):
      return HttpResponseRedirect('/arranger/profile')
    else:
      return f(*args, **kw) 
  return wrapper

def arrangerprofile(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ProfileForm(request.POST, instance=request.user.profile) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            form.save()
            return HttpResponseRedirect('/arranger/') # Redirect after POST
    else:
        form = ProfileForm(instance=request.user.profile) # An unbound form
    return render(request, 'arrangerprofile.html', {"form": form})
      

@login_required
@check_profile
def arrangerhome(request):
    return render(request, 'arrangerhome.html', {})

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
    

def makeamixdown(request):
    return render(request, 'displaysong.html', context)
    
