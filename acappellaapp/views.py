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

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        exclude = ('arranger','latlon', 'short_code', 'message')
        
class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class GroupForm(ModelForm):
    class Meta:
        model = Group
        exclude = ('arranger','latlon', 'short_code', 'message')

class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ('group', 'short_code', 'pdf_location')

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


@login_required
@check_profile
def arrangerhome(request):
  if request.method == 'POST': # If the form has been submitted...
    newgroup = Group(arranger=request.user.profile)
    form = GroupCreateForm(request.POST, instance=newgroup) # A form bound to the POST data
    if form.is_valid(): # All validation rules pass
      newgroup.short_code = newgroup.findshortcode(newgroup.name)
      form.save()
      return HttpResponseRedirect('/arranger/group/'+str(newgroup.short_code))
  else:
    form = GroupCreateForm()
  keywords = {"Groups": Group.objects.filter(arranger=request.user.profile), "GroupCreateForm": form }
  return render(request, 'arrangerhome.html', keywords)

@login_required
@check_profile
def arrangergrouphome(request, group_short_code):
  cur_group = Group.objects.get(short_code = group_short_code)
  if request.method == 'POST': # If the form has been submitted...
    if request.POST["__ACTION_TYPE"] == "D": #Delete Group
      cur_group.delete()
      return HttpResponseRedirect('/arranger/')
    if request.POST["__ACTION_TYPE"] == "N": #New Song
      newsong = Song(group=cur_group)
      songform = SongForm(request.POST, instance=newsong) # A form bound to the POST data
      if songform.is_valid(): # All validation rules pass
        newsong.short_code = newsong.findshortcode(cur_group, newsong.title)
        songform.save()
        return HttpResponseRedirect('/arranger/group/' + group_short_code + '/song/' + newsong.short_code)
      editform = GroupCreateForm(instance=cur_group)
    else: #EDIT
      editform = GroupCreateForm(request.POST, instance=cur_group) # A form bound to the POST data
      if editform.is_valid(): # All validation rules pass
        editform.save()
        del editform;
        editform = GroupCreateForm(instance=cur_group)
      songform = SongForm()
  else: #GET
    songform = SongForm()
    editform = GroupCreateForm(instance=cur_group)
  keywords = {"group":cur_group, "Songs": Song.objects.filter(group=cur_group), "NewSongForm": songform, "EditGroupForm": editform }
  return render(request, 'arrangergroup.html', keywords)


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
