from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import models
from .models import Team,Role,TeamMember,Timeline
from django.contrib.auth.models import User
from django import forms
from django.forms import modelformset_factory
from django.db.models import Q

def index(request):
	teamList=models.TeamMember.objects.filter(userName=request.user)
	print(teamList)
	teams=[]
	for team in teamList:
		teams.append(models.Team.objects.get(teamName = team.teamName))
	return render(request, 'viewTeams.html', {'teams':teams,'user':request.user})

def newTeam(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team=form.save(commit=False)
			team.created_date=timezone.now()
			team.teamLeader=request.user
			team.save()
			form2 = TeamMemberForm({'userName':request.user,'role':models.Role.objects.get(role='Team Leader')})
			if form2.is_valid():
				teamMembers=form2.save(commit=False)
				teamMembers.teamName=Team.objects.get(teamName=team.teamName)
				teamMembers.save()
				return redirect('addMembers',name=team.teamName)
	else:
		form = TeamForm(initial={'teamLeader':request.user})
		form.fields['teamLeader'].widget = forms.HiddenInput()
	return render(request, 'newTeam.html', {'form': form})

def addMembers(request,name):	
	form = modelformset_factory(TeamMember,form=TeamMemberForm,can_delete=True)
	memberList = models.TeamMember.objects.filter(teamName=name)
	if request.method == "POST":
		forms = form(request.POST)
		if forms.is_valid():
			for form in forms:
				print(form.cleaned_data)
				if form.cleaned_data["DELETE"]:
					if(form.cleaned_data["id"]):
						member=models.TeamMember.objects.get(Q(teamName=name) & Q(userName=form.cleaned_data["userName"]) )
						member.delete()
					print(str(form.cleaned_data)+" delete")
				else:
					teamMembers=form.save(commit=False)
					teamMembers.teamName=Team.objects.get(teamName=name)
					teamMembers.save()			
			return redirect('team')
	else:
		forms={'memberForms':form(queryset=memberList), }
	return render(request, 'addMembers.html', {'forms': forms})

def viewMembers(request,name):	
	memberList = models.TeamMember.objects.filter(teamName=name)
	return render(request, 'viewMembers.html', {'memberList': memberList})

def editTeam(request, name):
    team = get_object_or_404(models.Team, teamName=name)
    oldTeamLeader=team.teamLeader
    if request.method == "POST":
        form = TeamForm(request.POST,instance=team)
        if form.is_valid():
        	newTeam = form.save(commit=False)
        	newTeam.save()
        	if team.teamName!=newTeam.teamName:
	        	memberList = models.TeamMember.objects.filter(teamName=name)
	        	for member in memberList:
	        		member.teamName=Team.objects.get(teamName=newTeam.teamName)
	        		member.save()
	        	team = models.Team.objects.get(teamName=name)	
        		team.delete()
        	if oldTeamLeader!=newTeam.teamLeader:
        		print("leader changed")
        		leader = models.TeamMember.objects.filter(Q(teamName=newTeam.teamName) & Q(userName=request.user))
        		leader.delete()
        		existingMember=models.TeamMember.objects.get(Q(userName=newTeam.teamLeader) & Q(teamName=newTeam.teamName))
        		if existingMember:
        			existingMember.role=models.Role.objects.get(role='Team Leader')
        			existingMember.save()
        		else:
	        		form2 = TeamMemberForm({'userName':newTeam.teamLeader,'role':models.Role.objects.get(role='Team Leader')})
	        		if form2.is_valid():
	        			teamMembers=form2.save(commit=False)
	        			teamMembers.teamName=Team.objects.get(teamName=newTeam.teamName)
	        			teamMembers.save()
        	return redirect('team')
    else:
        form = TeamForm(instance=team)
    return render(request, 'teamDisplay.html', {'form': form ,})

def viewTeam(request,name):	
	team = models.Team.objects.get(teamName=name)
	return render(request, 'viewTeam.html', {'team': team})

def editTimeline(request,name):	
	form = modelformset_factory(Timeline,form=TimelineForm,can_delete=True)
	timelineList = models.Timeline.objects.filter(teamName=name)
	if request.method == "POST":
		forms = form(request.POST)
		if forms.is_valid():
			for form in forms:
				if(form.cleaned_data):
					if form.cleaned_data["DELETE"]:
							member=models.Timeline.objects.get(Q(teamName=name) & Q(task=form.cleaned_data["task"]) )
							member.delete()
					else:
						task=form.save(commit=False)
						task.teamName=Team.objects.get(teamName=name)
						print(task)
						task.save()			
			return redirect('team')
	else:
		forms={'timelineForms':form(queryset=timelineList), }
	return render(request, 'timeline.html', {'forms': forms})

def viewTimeline(request,name):	
	tasks = models.Timeline.objects.filter(teamName=name)
	return render(request, 'viewTimeline.html', {'tasks': tasks})