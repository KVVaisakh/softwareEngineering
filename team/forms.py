from django import forms
from .models import Team,TeamMember,Timeline

class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ('teamName', 'directoryLink',)

class TeamMemberForm(forms.ModelForm):

    class Meta:
        model = TeamMember
        fields = ('userName', 'role',)

class TimelineForm(forms.ModelForm):

    class Meta:
        model = Timeline
        fields = ('deadline', 'task','taskDetails')