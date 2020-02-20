from django.shortcuts import render
from django.http import HttpResponse
from .forms import TeamForm,TeamMemberForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import models
from .models import Team,TeamMember
from django import forms

def index(request):
	teams=models.Team.objects.filter(teamLeader=request.user)
	return render(request, 'viewTeams.html', {'teams':teams})
    # return HttpResponse("Create Team")

def enterTeamDetails(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team=form.save(commit=False)
			team.created_date=timezone.now()
			team.teamLeader=request.user
			team.save()			
			return redirect('index')
	else:
		form = TeamForm()
	return render(request, 'enterTeamDetails.html', {'form': form})

def addMembers(request,name):
	if request.method == "POST":
		form = TeamMemberForm(request.POST)
		if form.is_valid():
			teamMembers=form.save(commit=False)
			teamMembers.teamName=Team.objects.get(teamName=name)
			teamMembers.save()			
			return redirect('index')
	else:
		form = TeamMemberForm()
	return render(request, 'addMembers.html', {'form': form})

def teamDisplay(request,name):
	team = get_object_or_404(models.Team, teamName=name)
	members = get_object_or_404(models.teamMembers, pk=pk)
	return render(request, 'teamDisplay.html', {'team':team})

def teamEdit(request, name):
    team = get_object_or_404(models.Team, teamName=name)
    members = models.TeamMember.objects.filter(teamName=name)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.created_date = timezone.now()
            team.save()
            return redirect('teamDisplay', name=team.teamName)
    else:
        form = TeamForm(instance=team)
    return render(request, 'enterTeamDetails.html', {'form': form , 'members':members})