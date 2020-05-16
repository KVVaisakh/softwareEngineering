from django import forms
from .models import DirectMessage,GroupMessage
from django.contrib.auth.models import User

class DirectMessageFormM(forms.Form):
	message = forms.CharField(
		required = True,
		label = 'message',
		max_length = 100
	)
	sentTo = forms.CharField(
		required = True,
		label = 'sentTo',
		max_length = 100
	)

class DirectMessageForm(forms.ModelForm):

	class Meta:
		model = DirectMessage
		fields = ('sentTo','message',)

class GroupMessageForm(forms.ModelForm):

	class Meta:
		model = GroupMessage
		fields = ('sentTo','message',)

class UsernameForm(forms.ModelForm):

	class Meta:
		model = DirectMessage
		fields = ('sentTo',)
