from django import forms
from .models import DirectMessage,GroupMessage

class DirectMessageForm(forms.ModelForm):

    class Meta:
        model = DirectMessage
        fields = ('message')

class GroupMessageForm(forms.ModelForm):

    class Meta:
        model = GroupMessage
        fields = ('message')