# Create your views here.
from django.shortcuts import render
from acappellaapp.models import Group, Song, Track, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
import acappellasite.localsettings as localsettings
import json
import os
import random

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
    
@csrf_protect    
def displaysong(request, group_short_code, song_short_code):
    group = Group.objects.filter(short_code = group_short_code)[0]
    song = Song.objects.filter(short_code = song_short_code, group = group)[0]
    track_list = Track.objects.filter(song = song);
    context = {'group': group, 'song': song, 'track_list': track_list}
    return render(request, 'displaysong.html', context)
    

def makeamixdown(request, group_short_code, song_short_code):
    #create a list to include all temporary files
    tempfiles = []
    #create a random int to be used later
    rint = random.randint(1, 500000)
    #GET THE POST VALUES FROM REQUEST
    jsonstring = request.POST["json"]
    #CREATE AN OBJECT OUT OF THE DATA: "json"
    data = json.loads(jsonstring)
    #TODO: LATER HERE, ADD IN EFFECT PROCESSING
    #FROM THAT OBJECT DETERMINE WHAT GOES INTO THE LEFT CHANEL AND WHAT GOES INTO THE RIGHT CHANEL
    left, right = [], [];
    for track in data:
        if track["pan"] == "Center" or track["pan"] == "Left":
            left.append("static/user/tracks/"+track["filename"])
        if track["pan"] == "Center" or track["pan"] == "Right":
            right.append("static/user/tracks/"+track["filename"])

    if not left or not right: #Get sample rate of project if we need silence. 
        sr = os.popen('soxi -r ' + localsettings.basedir() + "static/user/tracks/" + data[0]["filename"]).read()
        sr = sr[:-1]
    
    #COMBINE LEFT CHANEL FILES AND RIGHT CHANEL FILES #TODO: I AM BREAKING (DRY)[wiki]. Factor this out.
    left_outputfile = localsettings.basedir() + "static/user/temp/LEFT_temp_"+str(rint)+".wav" 
    tempfiles.append(left_outputfile)
    if len(left) > 1:
        leftmixfiles = ""
        for a in left:
            leftmixfiles += localsettings.basedir() + a + " "
        leftmixcommand = "sox -m "+leftmixfiles+" "+left_outputfile
    if len(left) == 1:
        leftmixcommand = "sox "+ localsettings.basedir() + left[0]+" "+left_outputfile
    if len(left) == 0:
        leftmixcommand = "sox -n -r "+ sr +" "+left_outputfile+" trim 0.0 1"
    print(leftmixcommand)
    os.system(leftmixcommand)
    
    right_outputfile = localsettings.basedir() + "static/user/temp/RIGHT_temp_"+str(rint)+".wav" 
    tempfiles.append(right_outputfile)
    if len(right) > 1:
        rightmixfiles = ""
        for a in right:
            rightmixfiles += localsettings.basedir() + a + " "
        rightmixcommand = "sox -m "+rightmixfiles+" "+right_outputfile
    if len(right) == 1:
        rightmixcommand = "sox "+localsettings.basedir() + right[0]+" "+right_outputfile
    if len(right) == 0:
        rightmixcommand = "sox -n -r "+ sr +" "+right_outputfile+" trim 0.0 1"
    print(rightmixcommand)
    os.system(rightmixcommand)
    
    final_outputfile = localsettings.basedir() + "static/user/mixdowns/mixdown_"+str(rint)+".wav"
    final_outputfile_url = "/static/user/mixdowns/mixdown_"+str(rint)+".wav"
    finalremixcommand = "sox -M "+left_outputfile+" "+right_outputfile+" "+final_outputfile
    print(finalremixcommand)
    os.system(finalremixcommand)
    
    #Clean up any temporary files
    for afile in tempfiles:
        os.system("rm "+afile)
    
    #RESPOND WITH THE URL OF THE MIXDOWN FILE
    return HttpResponse(final_outputfile_url)
