from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ModelFormWithFileField
from team.models import Team,Timeline
from . import models
from django.shortcuts import redirect
from .models import File
from django.db.models import Q
import os

def index(request,name,task):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            file=form.save(commit=False)
            file.teamName=models.Team.objects.get(teamName=name)
            file.task=models.Timeline.objects.get(Q(teamName=name) & Q(task=task))
            file.save()
            return redirect('viewTimeline',name=name)
    else:
        form = ModelFormWithFileField()
        taskModel= models.Timeline.objects.get(Q(teamName=name) & Q(task=task))
        files=models.File.objects.filter(Q(teamName=name) & Q(task=taskModel))
        for file in files:
        	print(files)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    return render(request, 'upload.html', {'form': form,'files':files,'media':MEDIA_ROOT})