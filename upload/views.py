from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from team.models import *
from . import models
from django.shortcuts import redirect
from .models import File
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from tcs.decorators import *

@login_required
@userIsMember
@userIsDeveloper
def index(request,team,task):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            file=form.save(commit=False)
            file.uploaded_at=timezone.now()
            file.teamName=Team.objects.get(teamName=team)
            file.task=Timeline.objects.get(Q(teamName=team) & Q(task=task))
            file.file.name = team+"/"+task+"/"+request.user.username+"/"+file.name+"."+file.file.name.split(".")[-1]
            file.uploadedBy = request.user
            if File.objects.filter(Q(name=file.name) & Q(task=file.task) & Q(uploadedBy=file.uploadedBy)):
            	return render(request, 'upload.html', {'form': form,'name1':team,'task1':task})
            file.save()
            return redirect('viewTimeline',team=team)
    else:
        form = ModelFormWithFileField()        
    return render(request, 'upload.html', {'form': form,'name1':team,'task1':task})

@login_required
@userIsMember
def view(request,team,task):
    taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task))
    files=File.objects.filter(Q(teamName=team) & Q(task=taskModel))
    root = settings.MEDIA_URL    
    return render(request, 'view.html', {'files':files, 'root':root,})

@login_required
@userIsMember
@userIsTeamLeader
def grade(request,team,task):
    taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task))
    files=File.objects.filter(Q(teamName=team) & Q(task=taskModel))
    root = settings.MEDIA_URL
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            for file in files:
                if file.name in request.POST:
                    grade = File.objects.get(Q(name=file.name) & Q(task=file.task) & Q(uploadedBy=file.uploadedBy))
                    grade.grade=entry.grade
                    grade.save()
            return redirect('grade',team=team,task=task)
    else:
        form = GradeForm()
    return render(request, 'grade.html', {'form':form, 'files':files, 'root':root,})

@login_required
@userIsMember
@userIsDeveloper
def viewSuggestions(request,team,task,filename,uploadedBy):
    taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task) )
    user= User.objects.get(username=uploadedBy)
    file=File.objects.get(Q(teamName=team) & Q(task=taskModel) & Q(name=filename) & Q(uploadedBy=user))
    suggestions = Suggestion.objects.filter(file=file)
    return render(request, 'viewSuggestions.html', {'suggestions':suggestions,})

@login_required
@userIsMember
@userIsTester
def suggest(request,team,task,filename,uploadedBy):
    if request.method == 'POST':
    	taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task) )
    	user= User.objects.get(username=uploadedBy)
    	file=File.objects.get(Q(teamName=team) & Q(task=taskModel) & Q(name=filename) & Q(uploadedBy=user))
    	form = SuggestionForm(request.POST)
    	if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.suggestedAt=timezone.now()
            suggestion.file=file
            suggestion.suggestedBy=request.user
            suggestion.save()
            return redirect('view',team=team,task=task)
    else:
    	form = SuggestionForm()
    return render(request, 'suggest.html', {'form':form,})

@login_required
@userIsMember
@userIsDeveloper
def viewApprove(request,team,task,filename,uploadedBy):
	taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task) )
	user= User.objects.get(username=uploadedBy)
	file=File.objects.get(Q(teamName=team) & Q(task=taskModel) & Q(name=filename) & Q(uploadedBy=user))
	approvals = Approval.objects.filter(file=file)
	return render(request, 'viewApprovals.html', {'approvals':approvals,})

@login_required
@userIsMember
@userIsTester
def approve(request,team,task,filename,uploadedBy):
	taskModel= Timeline.objects.get(Q(teamName=team) & Q(task=task))
	user= User.objects.get(username=uploadedBy)
	file=File.objects.get(Q(teamName=team) & Q(task=taskModel) & Q(name=filename) & Q(uploadedBy=user))
	if request.method == 'POST':
		form = ApprovalForm(request.POST)
		if form.is_valid():
			approve = form.save(commit=False)
			approve.approvedBy=request.user
			approve.approvedAt=timezone.now()
			approve.file=file
			approve.save()
			return redirect('view',team=team,task=task)
	else:
		form = ApprovalForm()
	return render(request, 'approve.html', {'form':form,})