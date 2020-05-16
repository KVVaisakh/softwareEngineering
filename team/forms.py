from django import forms
from .models import *
from django.db.models import Q
from django.forms import ModelChoiceField
from django.contrib.auth.models import User

class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('teamName', 'directoryLink','teamLeader')

class TeamForm2(forms.Form):
	teamName = forms.CharField(
		required = True,
		label = 'teamName',
		max_length = 50
	)
	directoryLink = forms.CharField(
		required = True,
		label = 'directoryLink',
		max_length = 50,
	)
	teamLeader = ModelChoiceField(queryset=User.objects.all())

class TeamMemberForm(forms.ModelForm):
	Role = ModelChoiceField(queryset=Role.objects.filter(~Q(role='Team Leader')), empty_label=None)
	class Meta:
		model = TeamMember
		fields = ('userName',)

class TeamMemberForm2(forms.ModelForm):
	class Meta:
		model = TeamMember
		fields = ('userName','role')

class TimelineForm(forms.ModelForm):

    class Meta:
        model = Timeline
        fields = ('deadline', 'task','taskDetails')

class GradeForm(forms.Form):
    grade = forms.CharField(max_length=100)

class UserDetailForm(forms.ModelForm):

    class Meta:
        model = UserDetail
        fields = ('mobile','address','photo','dob')
