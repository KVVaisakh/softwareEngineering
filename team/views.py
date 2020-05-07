from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from tcs.decorators import *
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from . import models
from .models import Team,Role,TeamMember,Timeline
from django.contrib.auth.models import User
from django import forms
from django.forms import modelformset_factory,formset_factory
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	teamList=models.TeamMember.objects.filter(userName=request.user)
	print(teamList)
	teams=[]
	for team in teamList:
		teams.append(models.Team.objects.get(teamName = team.teamName))
	return render(request, 'viewTeams.html', {'teams':teams,'user':request.user})

@login_required
def newTeam(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team=form.save(commit=False)
			team.created_date=timezone.now()
			team.teamLeader=request.user
			team.save()
			tl=models.Role.objects.get(role="Team Leader")
			member=TeamMember(teamName=team,userName=request.user,role=tl)
			member.save()
			return redirect('addMembers',name=team.teamName)
	else:
		form = TeamForm(initial={'teamLeader':request.user})
		form.fields['teamLeader'].widget = forms.HiddenInput()
	return render(request, 'newTeam.html', {'form': form})

@login_required
@userIsMember
@userIsTeamLeader
def addMembers(request,team):	
	# form = modelformset_factory(TeamMember,form=TeamMemberForm,can_delete=True)
	tl=models.Role.objects.get(role="Team Leader")
	memberList = models.TeamMember.objects.filter(Q(teamName=team) & ~Q(role=tl))
	if memberList:
		form = formset_factory(form=TeamMemberForm,can_delete=True,extra = 0)
	else:
		form = formset_factory(form=TeamMemberForm,can_delete=True,extra = 1)
	if request.method == "POST":
		forms = form(request.POST)
		if forms.is_valid():
			for form in forms:
				print(form.cleaned_data)
				if form.cleaned_data["DELETE"]:
					member=models.TeamMember.objects.get(Q(teamName=team) & Q(userName=form.cleaned_data["userName"]) )
					member.delete()
					print(str(form.cleaned_data)+" delete")
				else:
					teamMember=form.save(commit=False)
					print(teamMember.userName)
					user= models.User.objects.get(username=teamMember.userName)
					member=models.TeamMember.objects.filter(Q(teamName=team) & Q(userName=form.cleaned_data["userName"]) )
					
					if member:
						member = get_object_or_404(models.TeamMember, teamName=team,userName=user)
						member.role=form.cleaned_data["Role"]
						member.save()
					else:
						teamMember.teamName=Team.objects.get(teamName=team)
						teamMember.role=form.cleaned_data["Role"]
						teamMember.save()
			return redirect('team')
	else:
		forms=form(initial=[{'Role':member.role,'userName':member.userName} for member in memberList])
		# forms=[]
		# for member in memberList:
		# 	forms.append(TeamMemberForm(initial={'Role':member.role, 'userName':member.userName}))
		# forms={'memberForms':forms  }
	return render(request, 'addMembers.html', {'forms': forms})

@login_required
@userIsMember
def viewMembers(request,team):	
	memberList = models.TeamMember.objects.filter(teamName=team)
	return render(request, 'viewMembers.html', {'memberList': memberList})

@login_required
@userIsMember
@userIsTeamLeader
def editTeam(request, team):
    team = get_object_or_404(models.Team, teamName=team)
    oldTeamLeader=team.teamLeader
    if request.method == "POST":
        form = TeamForm(request.POST,instance=team)
        if form.is_valid():
        	newTeam = form.save(commit=False)
        	newTeam.save()
        	if team.teamName!=newTeam.teamName:
	        	memberList = models.TeamMember.objects.filter(teamName=team)
	        	for member in memberList:
	        		member.teamName=Team.objects.get(teamName=newTeam.teamName)
	        		member.save()
	        	team = models.Team.objects.get(teamName=team)	
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

@login_required
@userIsMember
def viewTeam(request,team):	
	team = models.Team.objects.get(teamName=team)
	return render(request, 'viewTeam.html', {'team': team})

@login_required
@userIsMember
@userIsTeamLeader
def editTimeline(request,team):	
	form = modelformset_factory(Timeline,form=TimelineForm,can_delete=True)
	timelineList = models.Timeline.objects.filter(teamName=team)
	if request.method == "POST":
		forms = form(request.POST)
		if forms.is_valid():
			for form in forms:
				if(form.cleaned_data):
					if form.cleaned_data["DELETE"]:
							member=models.Timeline.objects.get(Q(teamName=team) & Q(task=form.cleaned_data["task"]) )
							member.delete()
					else:
						task=form.save(commit=False)
						task.teamName=Team.objects.get(teamName=team)
						print(task)
						task.save()			
			return redirect('team')
	else:
		forms={'timelineForms':form(queryset=timelineList), }
	return render(request, 'timeline.html', {'forms': forms})

@login_required
@userIsMember
def viewTimeline(request,team):	
	tasks = models.Timeline.objects.filter(teamName=team)
	return render(request, 'viewTimeline.html', {'tasks': tasks})